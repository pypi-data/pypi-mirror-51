#    Copyright 2017 MDSLAB - University of Messina All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

__author__ = "Nicola Peditto <n.peditto@gmail.com>"

# Autobahn imports
from autobahn.asyncio.component import Component
from autobahn.wamp import exception

# OSLO imports
from oslo_config import cfg
from oslo_log import log as logging

# MODULES imports
import asyncio
import inspect
import os
import pkg_resources
import signal
import ssl
import sys
import time
import txaio

from pip._vendor import pkg_resources
from stevedore import extension

# IoTronic imports
from iotronic_lightningrod.Board import Board
from iotronic_lightningrod.common.exception import timeoutALIVE
from iotronic_lightningrod.common.exception import timeoutRPC
from iotronic_lightningrod.common import utils
from iotronic_lightningrod.modules import utils as lr_utils
import iotronic_lightningrod.wampmessage as WM


# Global variables
LOG = logging.getLogger(__name__)

CONF = cfg.CONF

# LR options
lr_opts = [
    cfg.StrOpt('lightningrod_home',
               default='/var/lib/iotronic',
               help=('Lightning-rod Home Data')
               ),
    cfg.BoolOpt('skip_cert_verify',
                default=True,
                help=('Flag for skipping the verification of the server cert '
                      '(for the auto-signed ones)')
                ),
    cfg.StrOpt('log_level',
               default='info',
               help=('Lightning-rod log level')
               ),
]

CONF.register_opts(lr_opts)


# Autobahn options
autobahn_opts = [
    cfg.IntOpt('connection_timer',
               default=10,
               help=('IoTronic connection RPC timer')),
    cfg.IntOpt('alive_timer',
               default=600,
               help=('Wamp websocket check time')),
    cfg.IntOpt('rpc_alive_timer',
               default=3,
               help=('RPC alive response time threshold')),
    cfg.IntOpt('connection_failure_timer',
               default=600,
               help=('IoTronic connection failure timer')),
]

autobahn_group = cfg.OptGroup(
    name='autobahn', title='Autobahn options'
)
CONF.register_group(autobahn_group)
CONF.register_opts(autobahn_opts, group=autobahn_group)


# Options registration
logging.register_options(CONF)
DOMAIN = "s4t-lightning-rod"
CONF(project='iotronic')
logging.setup(CONF, DOMAIN)


# Logging setup
txaio.start_logging(level=str(CONF.log_level))


global SESSION
SESSION = None

global lr_cty
lr_cty = {}

global wport
wport = None

global board
board = None

from threading import Timer
global connFailure
connFailure = None
global connFailureBoot
connFailureBoot = None

reconnection = False
RPC = {}
RPC_devices = {}
RPC_proxies = {}
zombie_alert = True

# ASYNCIO
global loop
loop = None
component = None

RUNNER = None
connected = False

global MODULES
MODULES = {}


class LightningRod(object):

    def __init__(self):

        """
        LogoLR()

        LOG.info(' - version: ' +
                 str(utils.get_version("iotronic-lightningrod")))
        LOG.info(' - PID: ' + str(os.getpid()))

        LOG.info("LR available modules: ")
        for ep in pkg_resources.iter_entry_points(group='s4t.modules'):
            LOG.info(" - " + str(ep))

        logging.register_options(CONF)
        DOMAIN = "s4t-lightning-rod"
        CONF(project='iotronic')
        logging.setup(CONF, DOMAIN)

        if CONF.debug:
            txaio.start_logging(level="debug")
        """

        self.w = None

        # Manage LR exit signals
        signal.signal(signal.SIGINT, self.stop_handler)

        LogoLR()

        LOG.info('Lightning-rod: ')
        LOG.info(' - version: ' +
                 str(utils.get_version("iotronic-lightningrod")))
        LOG.info(' - PID: ' + str(os.getpid()))
        LOG.info(" - Home: " + CONF.lightningrod_home)

        if (CONF.log_file == "None"):
            LOG.info(' - Log file: not specified!')
        else:
            LOG.info(' - Log file: ' + CONF.log_file)
        LOG.info(" - Log level: " + str(CONF.log_level))

        LOG.info('Autobahn: ')
        LOG.info(" - Alive Check timer: " + str(CONF.autobahn.alive_timer) +
                 " seconds")
        LOG.info(" - RPC-Alive Check timer: "
                 + str(CONF.autobahn.rpc_alive_timer) + " seconds")
        LOG.info(" - Connection RPC timer: " + str(
            CONF.autobahn.connection_timer) + " seconds")
        LOG.info(" - Connection Faliure timeout: " + str(
            CONF.autobahn.connection_failure_timer) + " seconds")

        global board
        board = Board()

        # Start REST server
        singleModuleLoader("rest", session=None)

        if(board.status == "first_boot"):

            os.system("pkill -f 'node /usr/bin/wstun'")
            LOG.debug("OLD tunnels cleaned!")
            print("OLD tunnels cleaned!")

            LOG.info("LR FIRST BOOT: waiting for first configuration...")

        while (board.status == "first_boot"):
            time.sleep(5)

            # LR was configured and we have to load its new configuration
            board.loadSettings()

        # Start timer checks on wamp connection
        def timeout():
            LOG.warning("WAMP Connection failure timer onBoot: EXPIRED")
            lr_utils.LR_restart()

        global connFailureBoot
        connFailureBoot = Timer(
            CONF.autobahn.connection_failure_timer, timeout
        )
        connFailureBoot.start()
        LOG.info("WAMP Connection failure timer onBoot: STARTED")

        # Start Wamp Manager
        self.w = WampManager(board.wamp_config)
        self.w.start()

    def stop_handler(self, signum, frame):

        try:

            zombie_alert = False  # No zombie alert activation

            LOG.info("LR is shutting down...")
            if self.w != None:
                self.w.stop()

            Bye()

        except Exception as e:
            LOG.error("Error closing LR")


class WampManager(object):
    """WAMP Manager: through this LR manages the connection to Crossbar server.

    """

    def __init__(self, wamp_conf):

        # wampConnect configures and manages the connection to Crossbar server.
        wampConnect(wamp_conf)

    def start(self):
        LOG.info(" - starting Lightning-rod WAMP server...")
        try:
            if(board.status != "url_wamp_error"):
                global loop
                loop = asyncio.get_event_loop()
                component.start(loop)
                loop.run_forever()

        except Exception as err:
            LOG.error(" - Error starting asyncio-component: " + str(err))

    def stop(self):
        LOG.info("Stopping WAMP agent server...")
        # Canceling pending tasks and stopping the loop
        asyncio.gather(*asyncio.Task.all_tasks()).cancel()
        LOG.info("WAMP server stopped!")


def iotronic_status(board_status):

    if (board_status != "first_boot") \
            and (board_status != "already-registered") \
            and (board_status != "url_wamp_error"):

        # WS ALIVE
        try:
            alive = asyncio.run_coroutine_threadsafe(
                wamp_singleCheck(SESSION),
                loop
            )
            alive = alive.result()

        except Exception as e:
            LOG.error(" - Iotronic check: " + str(e))
            alive = e
    else:
        alive = "Not connected!"

    return alive


def wampNotify(session, board, w_msg, subject):

    rpc = str(board.agent) + u'.stack4things.notify_result'

    async def wampCall(session, board, wm, rpc, action):

        w_msg = None

        try:

            with timeoutRPC(seconds=10, action=action):
                res = await session.call(
                    rpc,
                    board_uuid=board.uuid,
                    wampmessage=wm
                )

            w_msg = WM.deserialize(res)

        except exception.ApplicationError as e:
            LOG.error(" - wampCall RPC error: " + str(e))

        LOG.debug(
            " - Notify result '" + subject + "': "
            + str(w_msg.result) + " - " + str(w_msg.message)
        )

        return w_msg

    res = asyncio.run_coroutine_threadsafe(
        wampCall(session, board, w_msg, rpc, "notify_result"),
        loop
    ).result()

    return res


async def wamp_singleCheck(session):
    try:

        # LOG.debug("ALIVE sending...")

        with timeoutALIVE(
                seconds=CONF.autobahn.rpc_alive_timer, action="ws_alive"):
            res = await session.call(
                str(board.agent) + u'.stack4things.wamp_alive',
                board_uuid=board.uuid,
                board_name=board.name
            )

        LOG.debug("WampCheck attempt " + str(res))

    except exception.ApplicationError as e:
        LOG.error(" - Iotronic Connection RPC error: " + str(e))

    return res


async def wamp_checks(session):

    while (True):

        try:

            # LOG.debug("ALIVE sending...")

            with timeoutALIVE(
                    seconds=CONF.autobahn.rpc_alive_timer, action="ws_alive"):
                res = await session.call(
                    str(board.agent) + u'.stack4things.wamp_alive',
                    board_uuid=board.uuid,
                    board_name=board.name
                )

            LOG.debug("WampCheck attempt " + str(res))

        except exception.ApplicationError as e:
            LOG.error(" - Iotronic Connection RPC error: " + str(e))
            # Iotronic is offline the board can not call
            # the "stack4things.alive" RPC.
            # The board will disconnect from WAMP agent and retry later.
            global reconnection
            reconnection = True
            lr_utils.destroyWampSocket()

        try:
            await asyncio.sleep(CONF.autobahn.alive_timer)
        except Exception as e:
            LOG.warning(" - asyncio alert: " + str(e))


async def IotronicLogin(board, session, details):
    """Function called to connect the board to Iotronic.

    The board:
     1. logs in to Iotronic
     2. loads the modules

    :param board:
    :param session:
    :param details:

    """

    LOG.info("IoTronic Authentication:")

    global reconnection

    try:

        rpc = str(board.agent) + u'.stack4things.connection'

        with timeoutRPC(seconds=CONF.autobahn.connection_timer, action=rpc):
            res = await session.call(
                rpc,
                uuid=board.uuid,
                session=details.session,
                info={
                    "lr_version": str(
                        utils.get_version("iotronic-lightningrod")
                    ),
                    "connectivity": lr_cty
                }

            )

            w_msg = WM.deserialize(res)

            if w_msg.result == WM.SUCCESS:

                LOG.info(" - Access granted to Iotronic.")

                # WS ALIVE
                asyncio.run_coroutine_threadsafe(wamp_checks(session), loop)

                # LOADING BOARD MODULES
                try:

                    modulesLoader(session)

                except Exception as e:
                    LOG.warning("WARNING - Could not load modules: " + str(e))
                    lr_utils.LR_restart()

                # Reset flag to False
                # reconnection = False

            else:
                Bye()

    except exception.ApplicationError as e:
        LOG.error(" - Iotronic Connection RPC error: " + str(e))
        # Iotronic is offline the board can not call
        # the "stack4things.connection" RPC.
        # The board will disconnect from WAMP agent and retry later.
        reconnection = True

        # We restart Lightning-rod if RPC 'stack4things.connection' is not
        # available, this means Wagent is unreachable
        lr_utils.LR_restart()

    except Exception as e:
        LOG.warning("Iotronic board connection error: " + str(e))
        reconnection = True
        # We restart Lightning-rod if RPC 'stack4things.connection'
        # returns generic errors
        lr_utils.LR_restart()


def wampConnect(wamp_conf):
    """WAMP connection procedures.

    :param wamp_conf: WAMP configuration from settings.json file

    """

    LOG.info("WAMP connection precedures:")

    try:

        LOG.info(
            "WAMP status @ boot:" +
            "\n- board = " + str(board.status) +
            "\n- reconnection = " + str(reconnection) +
            "\n- connected = " + str(connected)
        )

        wamp_transport = wamp_conf['url']
        wurl_list = wamp_transport.split(':')
        is_wss = False

        if wurl_list[0] == "wss":
            is_wss = True

        whost = wurl_list[1].replace('/', '')

        global wport
        wport = int(wurl_list[2].replace('/', ''))

        if is_wss and CONF.skip_cert_verify:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            wamp_transport = [
                {
                    "url": wamp_transport,
                    "max_retries": -1,
                    "serializers": ["json"],
                    "endpoint": {
                        "type": "tcp",
                        "host": whost,
                        "port": wport,
                        "tls": ctx
                    },
                },
            ]

        # LR creates the Autobahn Asyncio Component that points to the
        # WAMP Agent (main/registration agent)
        global component
        component = Component(
            transports=wamp_transport,
            realm=wamp_conf['realm']
        )

        # To manage the registration stage: we got the info for the main
        # WAMP agent and LR is going to connect to it starting the Component
        # with the new WAMP configuration.
        if connected == False and board.status == "registered" \
                and reconnection == False:
            try:
                component.start(loop)
            except Exception as err:
                LOG.error(" - Error connecting asyncio-component: " + str(err))

        @component.on_join
        async def join(session, details):
            """Execute the following procedures when the board connects
            to Crossbar.

            :param details: WAMP session details

            """

            global wport
            global lr_cty
            sock_bundle = lr_utils.get_socket_info(wport)

            if sock_bundle == "N/A":
                lr_cty = {}
            else:
                lr_cty['iface'] = sock_bundle[0]
                lr_cty['local_ip'] = sock_bundle[1]
                lr_cty['mac'] = sock_bundle[2]
                print(" - Selected NIC: " + str(lr_cty))

            global connected
            connected = True

            # LIGHTNING-ROD STATES:
            # - REGISTRATION STATE: the first connection to Iotronic
            # - FIRST CONNECTION: the board become operative after registration
            # - LIGHTNING-ROD BOOT: the first connection to WAMP
            #                       after Lightning-rod starting
            # - WAMP RECOVERY: when the established WAMP connection fails

            global reconnection

            # reconnection flag is False when the board is:
            # - LIGHTNING-ROD BOOT
            # - REGISTRATION STATE
            # - FIRST CONNECTION
            #
            # reconnection flag is True when the board is:
            # - WAMP RECOVERY

            global SESSION
            SESSION = session
            # LOG.debug(" - session: " + str(details))

            board.session_id = details.session

            # Clean Connection WAMP timers ------------------------------------
            global connFailure
            if connFailure != None:
                LOG.warning(
                    "WAMP Connection Failure timer: CANCELLED (onJoin)"
                )
                connFailure.cancel()

            global connFailureBoot
            if connFailureBoot != None:
                LOG.warning(
                    "WAMP Connection Failure timer onBoot: CANCELLED (onJoin)"
                )
                connFailureBoot.cancel()
            # -----------------------------------------------------------------

            LOG.info(" - Joined in realm " + board.wamp_config['realm'] + ":")
            LOG.info("   - WAMP Agent: " + str(board.agent))
            print(" - WAMP Agent: " + str(board.agent) + " - "
                  + str(wamp_conf['url']))
            LOG.info("   - Session ID: " + str(board.session_id))
            print(" - Session ID: " + str(board.session_id))
            LOG.info("   - Board status:  " + str(board.status))

            if sock_bundle == "N/A":
                LOG.info("   - Socket info:" + str(sock_bundle))
            else:
                LOG.info("   - Socket info: %s %s %s",
                         str(sock_bundle[0]),
                         str(sock_bundle[1]),
                         str(sock_bundle[2])
                         )

            if reconnection is False:

                if board.uuid is None:

                    ######################
                    # REGISTRATION STATE #
                    ######################
                    # If in the LR configuration file there is not the
                    # Board UUID specified it means the board is a new one
                    # and it has to call IoTronic in order to complete
                    # the registration.

                    try:

                        LOG.info(" - Board needs to be registered.")

                        rpc = u'stack4things.register'

                        with timeoutRPC(seconds=5, action=rpc):
                            res = await session.call(
                                rpc,
                                code=board.code,
                                session=board.session_id
                            )

                        w_msg = WM.deserialize(res)

                        # LOG.info(" - Board registration result: \n" +
                        #         json.loads(w_msg.message, indent=4))

                        if w_msg.result == WM.SUCCESS:

                            LOG.info("Registration authorized by IoTronic:\n"
                                     + str(w_msg.message))

                            # the 'message' field contains
                            # the board configuration to load
                            board.setConf(w_msg.message)

                            # We need to disconnect the client from the
                            # registration-agent in order to reconnect
                            # to the WAMP agent assigned by Iotronic
                            # at the provisioning stage
                            LOG.info(
                                "\n\nDisconnecting from Registration Agent "
                                "to load new settings...\n\n")

                            # We restart Lightning-rod if RPC
                            # 'stack4things.connection' is not available,
                            # this means Wagent is unreachable
                            lr_utils.LR_restart()

                        else:
                            LOG.error("Registration denied by Iotronic - " +
                                      "board already registered: "
                                      + str(w_msg.message))
                            board.status = "already-registered"
                            # Bye()

                    except exception.ApplicationError as e:
                        LOG.error("IoTronic registration error: " + str(e))
                        # Iotronic is offline the board can not call the
                        # "stack4things.connection" RPC. The board will
                        # disconnect from WAMP agent and retry later.

                        # TO ACTIVE BOOT CONNECTION RECOVERY MODE
                        reconnection = True

                        # We restart Lightning-rod if RPC
                        # 'stack4things.connection' is not available,
                        # this means Wagent is unreachable
                        lr_utils.LR_restart()

                    except Exception as e:
                        LOG.warning(
                            " - Board registration call error: " + str(e))
                        Bye()

                else:

                    if board.status == "registered":
                        ####################
                        # FIRST CONNECTION #
                        ####################

                        # In this case we manage the first connection
                        # after the registration stage:
                        # Lightining-rod sets its status to "operative"
                        # completing the provisioning and configuration stage.
                        LOG.info("\n\n\nBoard is becoming operative...\n\n\n")
                        board.updateStatus("operative")
                        board.loadSettings()
                        LOG.info("WAMP status @ first connection:" +
                                 "\n- board = " + str(board.status) +
                                 "\n- reconnection = " + str(reconnection) +
                                 "\n- connected = " + str(connected)
                                 )
                        await IotronicLogin(board, session, details)

                    elif board.status == "operative":
                        ######################
                        # LIGHTNING-ROD BOOT #
                        ######################

                        # After join to WAMP agent, Lightning-rod will:
                        # - authenticate to Iotronic
                        # - load the enabled modules

                        # The board will keep at this stage until
                        # it will succeed to connect to Iotronic.
                        await IotronicLogin(board, session, details)

                    else:
                        LOG.error("Wrong board status '" + board.status + "'.")
                        Bye()

            else:

                #################
                # WAMP RECOVERY #
                #################

                LOG.info("IoTronic connection recovery:")

                try:

                    rpc = str(board.agent) + u'.stack4things.connection'

                    with timeoutRPC(
                            seconds=CONF.autobahn.connection_timer, action=rpc
                    ):
                        res = await session.call(
                            rpc,
                            uuid=board.uuid,
                            session=details.session,
                            info={
                                "lr_version": str(
                                    utils.get_version("iotronic-lightningrod")
                                ),
                                "connectivity": lr_cty
                            }

                        )

                    w_msg = WM.deserialize(res)

                    if w_msg.result == WM.SUCCESS:

                        LOG.info(" - Access granted to Iotronic (recovery).")

                        # LOADING BOARD MODULES
                        # If the board is in WAMP connection recovery state
                        # we need to register again the RPCs of each module
                        try:

                            moduleReloadInfo(session)

                            # Reset flag to False
                            reconnection = False

                            LOG.info("WAMP Session Recovered!")

                            LOG.info("\n\nListening...\n\n")

                            # WS ALIVE
                            asyncio.run_coroutine_threadsafe(
                                wamp_checks(session),
                                loop
                            )

                        except Exception as e:
                            LOG.warning(
                                "WARNING - Could not reload modules: "
                                + str(e))
                            Bye()

                    else:
                        LOG.error("Access to IoTronic denied: "
                                  + str(w_msg.message))
                        Bye()

                except exception.ApplicationError as e:
                    LOG.error("IoTronic connection error:\n" + str(e))
                    # Iotronic is offline the board can not call
                    # the "stack4things.connection" RPC.
                    # The board will disconnect from WAMP agent and retry later

                    # TO ACTIVE WAMP CONNECTION RECOVERY MODE
                    reconnection = False

                    # We restart Lightning-rod if RPC 'stack4things.connection'
                    # is not available, this means Wagent is unreachable
                    lr_utils.LR_restart()

                except Exception as e:
                    LOG.warning("Board connection error after WAMP recovery: "
                                + str(e))
                    Bye()

        @component.on_leave
        async def onLeave(session, details):
            LOG.warning("WAMP Session Left: reason = " + str(details.reason))

        @component.on_connectfailure
        async def onConnectFailure(session, fail_msg):
            LOG.warning("WAMP Connection Failure: " + str(fail_msg))

            LOG.warning(" - timeout set @ " +
                        str(CONF.autobahn.connection_failure_timer))

            global connFailure
            if connFailure != None:
                LOG.warning("WAMP Connection Failure timer: CANCELLED")
                connFailure.cancel()

            def timeout():
                LOG.warning("WAMP Connection Failure timer: EXPIRED")
                lr_utils.LR_restart()

            connFailure = Timer(
                CONF.autobahn.connection_failure_timer, timeout
            )
            connFailure.start()
            LOG.warning("WAMP Connection Failure timer: STARTED")

        @component.on_disconnect
        async def onDisconnect(session, was_clean):
            """Procedure triggered on WAMP connection lost.
            :param session:
            :param was_clean:
            :return:
            """

            LOG.warning('WAMP Transport Left: was_clean = ' + str(was_clean))
            global connected
            connected = False

            global reconnection

            LOG.info(
                "WAMP status on disconnect:" +
                "\n- board = " + str(board.status) +
                "\n- reconnection = " + str(reconnection) +
                "\n- connected = " + str(connected)
            )

            board.session_id = "N/A"

            if board.status == "operative" and reconnection is False:

                #################
                # WAMP RECOVERY #
                #################
                # we need to recover wamp session and
                # we set reconnection flag to True in order to activate
                # the module-RPCs registration procedure for each module

                reconnection = True

                # LR needs to reconncet to WAMP
                if not connected:
                    LOG.warning(".............WAMP DISCONNECTION.............")
                    LOG.info(
                        "WAMP status on disconnect:" +
                        "\n- board = " + str(board.status) +
                        "\n- reconnection = " + str(reconnection) +
                        "\n- connected = " + str(connected)
                    )

                    # component.start(loop)

            elif board.status == "operative" and reconnection is True:

                ######################
                # LIGHTNING-ROD BOOT #
                ######################
                # At this stage if the reconnection flag was set to True
                # it means that we forced the reconnection procedure
                # because of the board is not able to connect to IoTronic
                # calling "stack4things.connection" RPC...
                # it means IoTronic is offline!

                # We need to reset the reconnection flag to False in order to
                # do not enter in module-RPCs registration procedure...
                # At this stage the board tries to reconnect to
                # IoTronic until it will come online again.
                reconnection = False

                # LR needs to reconncet to WAMP
                LOG.warning(".............WAMP DISCONNECTION.............")
                LOG.info("WAMP status on disconnect:" +
                         "\n- board = " + str(board.status) +
                         "\n- reconnection = " + str(reconnection) +
                         "\n- connected = " + str(connected)
                         )

                # component.start(loop)

            elif (board.status == "registered"):
                ######################
                # REGISTRATION STATE #
                ######################

                # LR was disconnected from Registration Agent
                # in order to connect it to the assigned WAMP Agent.

                LOG.debug("\n\nReconnecting after registration...\n\n")

                # LR load the new configuration and gets the new WAMP Agent
                board.loadSettings()

                # LR has to connect to the assigned WAMP Agent
                wampConnect(board.wamp_config)

            else:
                LOG.error("Reconnection wrong status!")

    except IndexError as err:
            LOG.error(" - Error parsing WAMP url: " + str(err))
            LOG.error(" --> port or address not specified")
            board.status = "url_wamp_error"

    except Exception as err:
        LOG.error(" - WAMP connection error: " + str(err))
        # Bye()


def moduleWampRegister(session, meth_list):
    """This function register for each module methods the relative RPC.

    :param session:
    :param meth_list:

    """

    if len(meth_list) == 2:

        LOG.info("   - No procedures to register!")

    else:

        for meth in meth_list:
            # We don't considere the "__init__", "finalize" and
            # "restore" methods
            if (meth[0] != "__init__") & (meth[0] != "finalize") \
                    & (meth[0] != "restore"):

                rpc_addr = u'iotronic.' + str(board.session_id) + '.' + \
                           board.uuid + '.' + meth[0]

                if not meth[0].startswith('_'):
                    session.register(meth[1], rpc_addr)
                    LOG.info("   --> " + str(meth[0]))


def singleModuleLoader(module_name, session=None):
    ep = []

    for ep in pkg_resources.iter_entry_points(group='s4t.modules'):
        # LOG.info(" - " + str(ep))
        pass

    if not ep:

        LOG.info("No modules available!")
        sys.exit()

    else:
        modules = extension.ExtensionManager(
            namespace='s4t.modules',
            # invoke_on_load=True,
            # invoke_args=(session,),
        )

        LOG.info('Module "' + module_name + '" loading:')

        for ext in modules.extensions:

            if (ext.name == 'rest'):

                mod = ext.plugin(board, session)

                global MODULES
                MODULES[mod.name] = mod

                # Methods list for each module
                meth_list = inspect.getmembers(mod, predicate=inspect.ismethod)

                global RPC
                RPC[mod.name] = meth_list

                if len(meth_list) == 3:
                    # there are at least two methods for each module:
                    # "__init__" and "finalize"

                    LOG.info(" - No RPC to register for "
                             + str(ext.name) + " module!")

                else:
                    if(session != None):
                        LOG.info(" - RPC list of " + str(mod.name) + ":")
                        moduleWampRegister(SESSION, meth_list)

                # Call the finalize procedure for each module
                mod.finalize()


def modulesLoader(session):
    """Modules loader method thorugh stevedore libraries.

    :param session:

    """

    LOG.info("Available modules: ")

    ep = []

    for ep in pkg_resources.iter_entry_points(group='s4t.modules'):
        LOG.info(" - " + str(ep))

    if not ep:

        LOG.info("No modules available!")
        sys.exit()

    else:

        modules = extension.ExtensionManager(
            namespace='s4t.modules',
            # invoke_on_load=True,
            # invoke_args=(session,),
        )

        LOG.info('Modules to load:')

        for ext in modules.extensions:

            LOG.debug(ext.name)

            if (ext.name == 'gpio') & (board.type == 'server'):
                LOG.info("- GPIO module disabled for 'server' devices")

            else:

                if ext.name != "rest":

                    mod = ext.plugin(board, session)

                    global MODULES
                    MODULES[mod.name] = mod

                    # Methods list for each module
                    meth_list = inspect.getmembers(
                        mod, predicate=inspect.ismethod
                    )

                    global RPC
                    RPC[mod.name] = meth_list

                    if len(meth_list) == 3:
                        # there are at least two methods for each module:
                        # "__init__" and "finalize"

                        LOG.info(" - No RPC to register for "
                                 + str(ext.name) + " module!")

                    else:
                        LOG.info(" - RPC list of " + str(mod.name) + ":")
                        moduleWampRegister(SESSION, meth_list)

                    # Call the finalize procedure for each module
                    mod.finalize()

        LOG.info("Lightning-rod modules loaded.")
        LOG.info("\n\nListening...")


def moduleReloadInfo(session):
    """This function is used in the reconnection stage to register

    again the RPCs of each module and for device.

    :param session: WAMP session object.

    """

    LOG.info("\n\nModules reloading after WAMP recovery...\n\n")

    try:

        # Call module restore procedures and
        # register RPCs for each Lightning-rod module
        for mod_name in MODULES:
            LOG.info("- Registering RPCs for module " + str(mod_name))
            moduleWampRegister(session, RPC[mod_name])

            LOG.info("- Restoring module " + str(mod_name))
            MODULES[mod_name].restore()

        # Register RPCs for the device
        for dev in RPC_devices:
            LOG.info("- Registering RPCs for device " + str(dev))
            moduleWampRegister(session, RPC_devices[dev])

    except Exception as err:
        LOG.warning("Board modules reloading error: " + str(err))
        lr_utils.LR_restart()


def Bye():
    LOG.info("Bye!")
    os._exit(1)


def LogoLR():
    LOG.info('##############################')
    LOG.info('  Stack4Things Lightning-rod')
    LOG.info('##############################')


def main():
    LightningRod()

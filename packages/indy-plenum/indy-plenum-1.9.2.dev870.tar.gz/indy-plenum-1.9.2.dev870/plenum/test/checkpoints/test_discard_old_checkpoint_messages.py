from plenum.server.replica_validator_enums import ALREADY_STABLE
from stp_core.loop.eventually import eventually
from plenum.common.messages.node_messages import Checkpoint
from plenum.test.checkpoints.helper import chkChkpoints, chk_chkpoints_for_instance
from plenum.test.helper import checkDiscardMsg
from plenum.test.helper import sdk_send_random_and_check


def test_discard_checkpoint_msg_for_stable_checkpoint(chkFreqPatched, looper,
                                                      txnPoolNodeSet,
                                                      sdk_pool_handle,
                                                      sdk_wallet_client,
                                                      reqs_for_checkpoint):
    sdk_send_random_and_check(looper, txnPoolNodeSet, sdk_pool_handle,
                              sdk_wallet_client, reqs_for_checkpoint)
    for inst_id in txnPoolNodeSet[0].replicas.keys():
        looper.run(eventually(chk_chkpoints_for_instance, txnPoolNodeSet,
                              inst_id, 1, 0, retryWait=1))
    node1 = txnPoolNodeSet[0]
    rep1 = node1.replicas[0]
    oldChkpointMsg = rep1._consensus_data.checkpoints[0]
    rep1.send(oldChkpointMsg)
    recvReplicas = [n.replicas[0].stasher for n in txnPoolNodeSet[1:]]
    looper.run(eventually(checkDiscardMsg, recvReplicas, oldChkpointMsg,
                          ALREADY_STABLE, retryWait=1))

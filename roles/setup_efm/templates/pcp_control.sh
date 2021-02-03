#!/bin/bash

# function returns the Pgpool-II backend node-id for the given hostname
# and port number, And if the node-id is not found 255 is returned
# Arguments:
# 1- Hostname
# 2- Port (optional) if not provided, node-id of first matching
# hostname will be returned
function get_pgpool_nodeid_from_host {
	if [ -z "$1" ]; then
		echo "ERROR: hostname not provided"
		return 255
	fi
	#Now get the total number of nodes configured in Pgpool-II
	node_count=$($PGPOOL_PATH/pcp_node_count -U $PCP_USER -h $PCP_HOST -p $PCP_PORT -w)
	echo "INFO: searching node-id for $1:$2 from $node_count configured backends"
	i=0
	while [ $i -lt $node_count ];
	do
		nodeinfo=$($PGPOOL_PATH/pcp_node_info -U $PCP_USER -h $PCP_HOST -p $PCP_PORT -w $i)
		hostname=$(echo $nodeinfo | awk -v N=1 '{print $N}')
		port=$(echo $nodeinfo | awk -v N=2 '{print $N}')
		#if port number is <= 0 we just need to compare hostname
		if [ "$hostname" == $1 ] && ( [ -z "$2" ] || [ $port -eq $2 ] );
		then
			echo "INFO: $1:$2 has backend node-id = $i in Pgpool-II"
			return $i
		fi
		let i=i+1
	done
	return 255
}
# Function attach the node-id to the Pgpool-II
# Arguments
# 1- node-id: Pgpool-II backend node-id to be attached
function attach_node_id {
	if [ -z "$1" ]; then
		echo "ERROR: node-id not provided"
		return 255
	fi
	$PGPOOL_PATH/pcp_attach_node -w -U $PCP_USER -h $PCP_HOST -p $PCP_PORT $1
	return $?
}
# Function promotes the node-id to the new master node
# Arguments:
# 1- node-id: Pgpool-II backend node-id of node to be promoted to master
function promote_node_id_to_master {
	if [ -z "$1" ]; then
		echo "ERROR: node-id not provided"
		return 255
	fi
	$PGPOOL_PATH/pcp_promote_node -w -U $PCP_USER -h $PCP_HOST -p $PCP_PORT $1
	return $?
}

# function attaches the backend node identified by hostname:port
# to Pgpool-II
# Arguments:
# 1- Hostname
# 2- Port (optional) if not provided, node-id of first matching
# hostname will be promoted
#
function attach_node {
	get_pgpool_nodeid_from_host $1 $2
	node_id=$?
	if [ $node_id -eq 255 ]; then
		echo "ERROR: unable to find Pgpool-II backend node id for $1:$2"
		return 255
	else
		echo "INFO: attaching node-id: $node_id to Pgpool-II"
		attach_node_id $node_id
		return $?
	fi
}
# function promotes the standby node identified by hostname:port
# to the master node in Pgpool-II
# Arguments:
# 1- Hostname
# 2- Port (optional) if not provided, node-id of first matching
# hostname will be promoted
#
function promote_standby_to_master {
	get_pgpool_nodeid_from_host $1 $2
	node_id=$?
	if [ $node_id -eq 255 ]; then
		echo "ERROR: unable to find Pgpool-II backend node id for $1:$2"
		return 255
	else
		echo "INFO: promoting node-id: $node_id to master"
		promote_node_id_to_master $node_id
	return $?
	fi
}

function print_usage {
	echo "usage:"
	echo " $(basename $0) operation hostname [port]".
	echo " operations:".
	echo " attach: attach node".
	echo " promote: promote node".
}
# script entry point
if [ -z "$1" ] || [ -z "$2" ]; then
	echo "ERROR: operation not provided"
	print_usage
	exit 1
fi
shopt -s nocasematch
case "$1" in
	"attach" )
		attach_node $2 $3
	;;
	"promote" )
		promote_standby_to_master $2 $3
	;;
	*)
		echo "ERROR: invalid operation $1"
		print_usage
	;;
esac
exit $?

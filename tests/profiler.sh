#!/usr/bin/env bash

interpreter="python3"
alg="-mh"
file=''

usage(){
	echo "Usage: $0 puzzlefile [algorithm] [-pypy3]"
	exit 1
}

if [[ -f $1 ]]; then
	fullfile=$1
	file=$(basename -- "$1")
else
	usage
	exit 1
fi

while test $# != 0
do
    case "$1" in
    -pypy3) interpreter="pypy3" ;;
    -mh|-lc|-greedy)
        alg="$1"; shift ;;
    --) shift; break;;
    esac
    shift
done

o_file=cprof_${file}_alg${alg}_intperpreter-${interpreter}_$(date +%Y-%m-%d_at_%Hh%Ms%S).cprof

$interpreter -m cProfile -s cumtime -o $o_file ../n-puzzle.py $fullfile $alg
snakeviz $o_file
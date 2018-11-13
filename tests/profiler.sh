#!/usr/bin/env bash

interpreter="python3"
he="-he=mh"
file=''
oflag='-o '
o_file=''
alg='-a=astar'
visualizer="snakeviz"

usage(){
	printf "Usage: \n\t$0 puzzlefile [ -he=mh | -he=lc | -he=other heuristic flag ] [ -a=greedy ]\n\t$0 -d\n\n\t-d: deletes all .cprof files in this directory."
	exit 1
}

if [[ -f $1 ]]; then
	fullfile=$1
	file=$(basename -- "$1")
elif [[ $1 == "-d" ]]; then
	rm -f *.cprof
	printf "All profile output files removed."
	exit 1
else
	usage
	exit 1
fi

while test $# != 0
do
    case "$1" in
    -he=mh|-he=lc|-he=db|-he=mt)
        he="$1"; shift ;;
	-a=greedy)
        alg="$1"; shift ;;
    --) shift; break;;
    esac
    shift
done

o_file=cprof_${file}_${he}__$(date +%Y-%m-%d_at_%Hh%Ms%S).cprof

command -v $visualizer >/dev/null 2>&1 || { echo >&2 "You don't have snakeviz (pip3 install snakeviz); output will be printed to stdout instead."; o_file=''; oflag=''; visualizer=''; }

$interpreter -m cProfile -s cumtime $oflag$o_file ../n-puzzle.py $fullfile $he $alg
$visualizer $o_file
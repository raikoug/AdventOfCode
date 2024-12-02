#!/bin/bash
set -e

get_last_day() {
    # Trova l'ultimo giorno e rimuove eventuali zeri iniziali
    last_day=$(find ./ -type d -name 'day_*' | awk -F "_" '{print $2}' | sort -n | tail -n 1 | sed 's/^0*//')
    if [[ -z "$last_day" ]]; then
        echo "Errore: Nessuna directory 'day_' trovata nella directory corrente."
        exit 1
    fi
    echo "$last_day"
}


create_dir() {
    last_day=$(get_last_day)
    if ! [[ "$last_day" =~ ^[0-9]+$ ]]; then
        echo "Errore: 'last_day' non è un numero valido."
        exit 1
    fi
    new_day=$((last_day+1))
    dirname="day_$(printf "%02d" $new_day)"  # Formatta il nome con due cifre
    if [[ -d "$dirname" ]]; then
        echo "Errore: La directory '$dirname' esiste già."
        exit 1
    fi
    mkdir "$dirname"
    echo "$dirname"
}

create_files() {
    dirname=$(create_dir)
    if [[ -z "$dirname" ]]; then
        echo "Errore: 'dirname' non può essere vuoto."
        exit 1
    fi
    #touch "$dirname/instructions.md"
    last_day=$(get_last_day)
    filename="day_$(printf "%02d" $last_day)"

    cd /home/raikoug/SyncThing/SharedCodeTest/adventOfCode/2024/solutions/python
    cp day_00.py "$filename.py"
}

cd /home/raikoug/SyncThing/SharedCodeTest/adventOfCode/2024/inputs/ || {
    echo "Errore: Impossibile cambiare directory."
    exit 1
}

create_files

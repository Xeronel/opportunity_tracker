#!/bin/bash
# Parse Arguments
while [[ $# -gt 1 ]]
do
KEY="$1"
case ${KEY} in
    -v|--venv)
    VENV="$2"
    shift   # past argument
    ;;
    *)
            # unknown option
    ;;
esac
shift       # past argument or value
done

# Install css/js deps
bower install

# Install python deps
if [ -z "$VENV" ]; then
    sudo -H pip3.5 install -r requirements.txt
else
    ${VENV}/bin/pip3.5 install -r requirements.txt
fi

# Transpile scss to css
cd ./static/bower/datatables-buttons/css/
sass --update \
buttons.bootstrap.scss:buttons.bootstrap.css \
buttons.bootstrap4.scss:buttons.bootstrap4.css \
buttons.dataTables.scss:buttons.dataTables.css \
buttons.foundation.scss:buttions.foundation.css \
buttons.jqueryui.scss:buttons.jqueryui.css \
buttons.semanticui.scss:buttons.semanticui.css \
common.scss:common.css \
mixins.scss:mixins.css

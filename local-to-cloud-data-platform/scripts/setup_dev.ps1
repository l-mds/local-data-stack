$ProgressPreference = 'SilentlyContinue'
# Setup development environment: install tools and editable packages
python -m pip install -U pip setuptools wheel
python -m pip install -r "${PSScriptRoot.replace('/scripts','')}/requirements-dev.txt"
python -m pip install -e "${PSScriptRoot.replace('/scripts','')}/src/shared_library"
python -m pip install -e "${PSScriptRoot.replace('/scripts','')}/src/code_location_local_to_cloud_data_platform"
python -m pip install -e "${PSScriptRoot.replace('/scripts','')}/src/code_location_foo"
Write-Output "Development environment setup complete."

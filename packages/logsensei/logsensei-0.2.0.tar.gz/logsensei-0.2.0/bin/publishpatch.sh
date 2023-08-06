#!/usr/bin/env bash

bumpversion patch --tag --commit
git push
dotenv -f env/flit.env run flit publish
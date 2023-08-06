#!/usr/bin/env bash

bumpversion major --tag --commit
git push
dotenv -f env/flit.env run flit publish
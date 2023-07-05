@echo off
setlocal
cd frontend
if not exist node_modules\ (
  npm i
)
npm run --silent start

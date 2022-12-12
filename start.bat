cd frontend
if exist node_modules\ (
  echo Exists
) else (
  npm i
)
npm run start

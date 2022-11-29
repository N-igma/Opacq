cd frontend
[ "$(ls -A node_modules)" ] && echo "Not Empty" || npm install
npm run start

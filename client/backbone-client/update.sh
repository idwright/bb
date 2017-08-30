#curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
#sudo apt-get install -y nodejs
npm install @angular/{common,compiler,compiler-cli,core,forms,http,material,platform-browser,platform-browser-dynamic,router,animations}@latest typescript@latest @swimlane/ngx-datatable@latest rxjs@latest --save
npm install --save-dev @angular/cli@latest
rm package-lock.json
ng serve
rm -rf node_modules/
npm install


Paste your secret rsa key into /root/.ssh/id_rsa_secret
Then chmod the file r only by root
Then cd /opt
Then run: git clone git@secretgithub.com:DanielPuckett/DiallerSite-Secrets DiallerSite-Secrets
Then run sh setup.sh from that new directory

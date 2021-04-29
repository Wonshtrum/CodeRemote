const Discord = require('discord.js');
const client = new Discord.Client();
const config = require('./config.json');
const token = require('./token.json');
const axios = require('axios').default;
const fs = require('fs');


let prefix = config.prefix;
let status = ["SUCCESS", "COMPILATION_FAILED", "CRASHED", "LIMIT_REACHED","GENERIC_ERROR"]
let languages;

const lang_discord_to_api = {
    'py': 'python3',
    'python': 'python3',
    'cpp': 'c++',
  }
  const lang_to_ext = {
    'python3': '.py',
    'c++': '.cpp',
    'c': '.c',
    'java': '.java',
  }


//Log in pour le bot
client.on('ready', () => {
    client.user.setActivity(`${prefix}help`,{type:"PLAYING"});

    axios.get(`http://127.0.0.1:4382/languages`)
    .then(response => {
        languages = response.data.data;
        console.log('Les langages sont présents');
    })
    .catch(error => console.log(error));

    console.log(`Logged in as ${client.user.tag}!`);

});

let serverRequestTemplate = {
    "lang" : String,
    "files" : {
        "name" : String,
        "content" : String
    }
}

client.on('message', message =>{
    if (message.content.startsWith(`${prefix}`)) {
        let command = message.content.slice(prefix.length)

        if (command.startsWith('prefix')) {
            var newPrefix=message.content.slice(8);
            if (newPrefix.length==1){
                config.prefix=newPrefix; 
                let configJson = JSON.stringify(config);
                fs.writeFile('./config.json',configJson, (erreur) => {
                    if (erreur) console.log(erreur);
                    else message.channel.send (`Prefix has been changed to ${newPrefix}`);
                })
                prefix = config.prefix;
            } else {
                message.channel.send(`Prefix is still ${prefix}, prefix suggested not correct`);
            }
            client.user.setActivity(`${prefix}help`,{type:"PLAYING"});
        }

        if (command.startsWith('run')){

            let blocks = message.content.split('```', 3);

            if (blocks.length != 3) {
                message.channel.send('Manque un bout la');
                return;
            }

            let block = blocks[1];
            let firstNL = block.indexOf('\n');

            let language = block.substring(0, firstNL).toLowerCase();
            let cleanlanguage = lang_discord_to_api[language] || language;
            let code = block.substring(firstNL+1);
            let cleancode = Discord.Util.escapeCodeBlock(code);

            let ext = lang_to_ext[cleanlanguage] || ".txt";
                request = {
                    "lang" : cleanlanguage,
                    "files" : [{
                        "name" : "DiscordRequest"+ext,
                        "content" : cleancode
                    }]
            }

            if (languages.includes(cleanlanguage)) {
                
                axios.put(`http://127.0.0.1:4382/compile`,request)
                .then(response =>{ 
    
                    message.channel.send("Response API : "+ `${response.data.data.hash} \n`)
    
                    let hash = {hash : response.data.data.hash}; 
    
                        axios.post(`http://127.0.0.1:4382/result`,hash)
                        .then(response => {
                            message.channel.send("Status : " + `${status[response.data.data.logs.status]} \n`);
                            if (response.data.data.logs.message) {
                                message.channel.send("Message : " + `${response.data.data.logs.message} \n`);
                            }
                            if (response.data.data.logs) {
                                let logs = JSON.stringify(response.data.data.logs);
                                message.channel.send("Logs : " + `${logs} \n`);
                            }
                            if (response.data.data.stdout) {
                                let attachmentOut = new Discord.MessageAttachment(Buffer.from(response.data.data.stdout, 'utf-8'), 'stdout.txt');
                                message.channel.send('stdout:', attachmentOut);
                            }else{
                                message.channel.send('stdout est vide')
                            }
                            if (response.data.data.stderr.trim()) {
                                let attachmentErr = new Discord.MessageAttachment(Buffer.from(response.data.data.stderr, 'utf-8'), 'stderr.txt');
                                message.channel.send('stderr:', attachmentErr);
                            }else{
                                message.channel.send('stderr est vide')
                            }
                            console.log(response.data.data);
                        })
                        .catch(error => console.log(error));
                })
                .catch(error => console.log(error));
    
            }
            else{
                message.channel.send(`Le language : ${cleanlanguage} que vous avez entré n'est pas reconnu`);
            }

        }


        switch (command) {
            case "ping":
                var ping = Date.now() - message.createdTimestamp + "ms";
                message.channel.send("Your ping is " + `${ping} ` + " Pong !");
                break; 

            case "help":
                message.channel.send(`
                Voici une liste des commandes :

                **${prefix}help** - Afficher le menu d'aide
                **${prefix}ping** - Renvoie ton ping
                **${prefix}prefix [prefix]** - Change le préfix des commandes
                **${prefix}run code** - Run du code et renvoie le résultat
                **${prefix}languages** - Renvoie une liste des languages disponibles

                `)
                break;

            case "languages":
                axios.get(`http://127.0.0.1:4382/languages`)
                .then(response =>{
                    languages = response.data.data; 
                    message.channel.send("Voici une liste des languages disponibles : "+ `${response.data.data} \n`);
                })
                .catch(error => console.log(error));

                break;
            default:
                break;
        }
    }
})






client.login(token.token);
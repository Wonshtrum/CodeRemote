const Discord = require('discord.js');
const client = new Discord.Client();
const config = require('./config.json');
const token = require('./token.json');
const axios = require('axios').default;
const fs = require('fs');


let prefix = config.prefix;
let status = ["SUCCESS", "COMPILATION_FAILED", "CRASHED", "LIMIT_REACHED"]



//Log in pour le bot
client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

client.on('ready', () => {

    client.user.setActivity(`${prefix}help`,{type:"PLAYING"});
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

            //Bloc pour récupérer le language
            let language = message.content.split('\n');
            let cleanlanguage = language.shift().slice(8).split(' ')[0];

            //Bloc pour récupérer un string du code
            let code = message.content.split('\n');
            code.shift();
            code.pop();
            let code2 = code.join('\n');
            let cleancode = Discord.Util.escapeCodeBlock(code2);

            //sendtoserver(cleanlanguage,cleancode);
            //Construction de l'objet à envoyer a l'API
            let request = Object.create(serverRequestTemplate);
            request = {
                "lang" : cleanlanguage,
                "files" : [{
                    "name" : "Discord Request",
                    "content" : cleancode
                }]
            }
            axios.put(`http://127.0.0.1:4382/compile`,request)
            .then(response =>{ 

                message.channel.send("Response API : "+ `${response.data.data.hash} \n`)

                let hash = {hash : response.data.data.hash}; 

                    axios.post(`http://127.0.0.1:4382/result`,hash)
                    .then(response => {
                        message.channel.send("Status : " + `${status[response.data.data.logs.status]} \n`);
                        message.channel.send("Message : " + `${response.data.data.logs.message} \n`);

                        message.channel.send("```"+ `${response.data.data.stdout.slice(0,1900)} \n`+ "```");
                        message.channel.send("```"+ `${response.data.data.stderr.slice(0,1900)} \n`+ "```");
                    })
                    .catch(error => console.log(error));
            })
            .catch(error => console.log(error));

            

            
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
                .then(response => message.channel.send("Voici une liste des languages disponibles : "+ `${response.data.data} \n`))
                .catch(error => console.log(error));

                break;
            default:
                break;
        }
    }
})






client.login(token.token);
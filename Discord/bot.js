const Discord = require('discord.js');
const client = new Discord.Client();
const config = require('./config.json');
const axios = require('axios').default;
const fs = require('fs');


var prefix = config.prefix;
var languages = ['python3','c++','java','c'];


//Log in pour le bot
client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});


client.on('ready', () => {
    //var languages = axios.get('localhost:8080/languages');

    client.user.setActivity(`${prefix}help`,{type:"PLAYING"});
});



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
            //var codelanguage = message.content.slice(5);
            var codeString = message.content;
            let codearray = codeString.split('\n');
            codearray.splice().pop();
            let cleancode2 = codearray.join('\n');
            let cleancode = Discord.Util.escapeCodeBlock(cleancode2);
            //message.channel.send(`Le language selectionné est : ${codelanguage}`);
            message.channel.send(`${cleancode}`);
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


                `)
                break;
            default:
                break;
        }
    }
})

function getAPI() {
    
}





client.login(config.token);
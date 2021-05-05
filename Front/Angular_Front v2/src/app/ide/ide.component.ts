
import { AfterViewInit, Component, ElementRef, Input, ViewChild } from "@angular/core";
import {HttpClient} from '@angular/common/http';
import * as ace from "ace-builds";
import { NgbAlert } from "@ng-bootstrap/ng-bootstrap";
import {Subject} from 'rxjs';
import {debounceTime} from 'rxjs/operators';
export interface IAlert {
  id: number;
  type: string;
  strong?: string;
  message: string;
  icon?: string;
}

@Component({
  selector: 'app-ide',
  templateUrl: './ide.component.html',
  styleUrls: ['./ide.component.css']
})


export class IdeComponent implements AfterViewInit {
  public onOptionsSelected(event) {
    console.log(event);
    const aceEditor = ace.edit(this.editor.nativeElement);
    aceEditor.session.setMode("ace/mode/"+event);
  }
  @ViewChild("editor") private editor: ElementRef<HTMLElement>;


  ngOnInit(){

    
    this.http.get('http://127.0.0.1:4382/languages')
    .subscribe(response  => {
      this.response = response
      console.log(this.response)
      this.dropDownData = this.response.data
    });
 
  }
  ngAfterViewInit(): void {
    ace.config.set("fontSize", "14px");
    ace.config.set(
      "basePath",
      "https://unpkg.com/ace-builds@1.4.12/src-noconflict"
    );
    const aceEditor = ace.edit(this.editor.nativeElement);
    aceEditor.session.setValue(this.obj.files[0].content);
    aceEditor.setTheme("ace/theme/dracula");
    aceEditor.session.setMode("ace/mode/python");
    aceEditor.on("change", () => {
      var index = this.obj.files.map(function(o) { return o.name; }).indexOf(this.fileSelected);
      console.log(aceEditor.getValue());
      this.contentIDE= aceEditor.getValue();
      this.obj.files[index].content=this.contentIDE;
      console.log(this.contentIDE)
    });
  }
  datas ={
    "python3":"python",
    "c++":"c_cpp",
    "c":"c_cpp",
    "php":"php",
    "java":"java",
    "rust":"rust"
  }

  stock={}

  dropDownData ;
  response;
  contentIDE;
  hash;
  resultPost : any={
    "stdout": "Bloc Out",
    "stderr": "Bloc Err",
    "logs": {
      "id":0 ,
      "message": "string",
      "compilation_time": 0.222,
      "execution_time": 0.1111
    }
  };
  visible = false;



  alert: IAlert;


  nom="main.cpp";
  obj = {
    lang: "text",
    files: [
      {
        "name":this.nom,
        "content": "editFileName= Welcome to our compilator ",
        "edit":false
      }
    ]
  };
  fileSelected=this.nom;

  editFileName(item:any){
    var verifName = this.obj.files.filter(function(o) { return o.name==item.name});
    const aceEditor = ace.edit(this.editor.nativeElement);
    if(item.edit==false || (item.name.length>0 && verifName.length<2) ){
      item.edit=!item.edit;
      this.fileSelected=item.name;
      aceEditor.session.setValue(item.content);
    }

    
  }
  deletefile(item:any){
    this.obj.files.splice(this.obj.files.indexOf(item),1);
    const aceEditor = ace.edit(this.editor.nativeElement);
    aceEditor.session.setValue("");
 
  }
  showFile(item:any){


    this.fileSelected=item.name;
  

    const aceEditor = ace.edit(this.editor.nativeElement);
    aceEditor.session.setValue(item.content);
    console.log(this.fileSelected);
  }


  public newFile(){
    var values = this.obj.files.map(function(o) { return o.edit; });
    if (values.includes(true)){
      alert("Veuillez saisir un nom pour chaque fichier");
    }
    else{
      this.obj.files.push({name : "",content:"",edit:true});
      console.log(this.obj);
    }
  }

  
  public run(){
    var values = this.obj.files.map(function(o) { return o.edit; });
    if (values.includes(true)){
      alert("Veuillez saisir un nom pour chaque fichier");
    }
    else{
      var e = (document.getElementById("selectLangage")) as HTMLSelectElement;
      var strLangage = e.options[e.selectedIndex].text;

      const aceEditor = ace.edit(this.editor.nativeElement);
      console.log(aceEditor.getValue())
      console.log(strLangage);

      this.obj.lang=strLangage;
      console.log("----------------------------------");
      console.log(this.obj);
      console.log("----------------------------------");
      //console.log(data);
      console.log("rzrzerze")
      this.http.put('http://127.0.0.1:4382/compile',this.obj)
      .subscribe(response  => {
        this.hash = response
        this.hash = this.hash.data.hash
  
        console.log(this.hash)
        console.log(response)
        this.http.post('http://127.0.0.1:4382/result',{"hash":this.hash})
        .subscribe(response   => {
  
          this.resultPost=response
          this.resultPost = this.resultPost.data
          console.log(response)
         
          this.stock=this.alerts[this.resultPost.logs.status];
          this.visible=true;
        });
      });
      console.log("zeezrzerfsdf")
    }
    

  





    
  }



  @Input()
  public alerts: Array<IAlert> = [];
  private backup: Array<IAlert>;



  constructor(private http : HttpClient) {
      this.alerts.push({
          id: 0,
          type: 'success',
          strong: 'Success!',
          message: 'La compilation a réussi !',
          icon: 'ni ni-like-2'
      }, {
          id: 1,
          strong: 'Failed!',
          type: 'warning',
          message: 'Problème lors de la compilation!',
          icon: 'ni ni-bell-55'
      }, {
          id: 2,
          type: 'warning',
          strong: 'Warning!',
          message: 'L\'éxécution n\'a pas marché !',
          icon: 'ni ni-bell-55'
      }, {
          id: 3,
          type: 'danger',
          strong: 'Danger!',
          message: 'La compilation ou l\'éxécution du code a mis trop de temps pour s\'éxécuter!',
          icon: 'ni ni-support-16'
      },
      {
        id: 4,
        type: 'warning',
        strong: 'Erreur!',
        message: 'Erreur inconnue!',
        icon: 'ni ni-support-16'
    });
      this.backup = this.alerts.map((alert: IAlert) => Object.assign({}, alert));
  }

  close(alert: IAlert) {
    this.alerts.splice(this.alerts.indexOf(alert), 1);
  }
}
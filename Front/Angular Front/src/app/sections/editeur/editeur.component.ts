
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
  selector: "app-editeur",
  template: `
  
  <div class="container mb-5">
  <div class="col-lg-2 col-sm-2">


  <div class="form-group">
  <select class='select-option' 
    id ="selectLangage"
    #mySelect
    (change)='onOptionsSelected(mySelect.value)'>
   <option class='option' 
   *ngFor='let option of dropDownData' 
   [value]="datas[option] || 'text'">{{option}}</option>
</select>
  </div>
  </div>
  <div style="display:flex;">

    <div  class="overflow-scroll" style="max-height : 500px;width : 100px;">
    <ul id="listFileName" style="list-style-type:none;padding:0;padding-right:1em;" >
      <li  *ngFor="let item of obj.files">
      <div style="float:right;" *ngIf=!item.edit (click)="deletefile()"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
      <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
      <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
    </svg></div>
        <div id="{{ item.name }}" (dblclick)="editFileName(item)"(click)="showFile(item)" *ngIf=!item.edit style="text-overflow: ellipsis;
        overflow: hidden;">{{ item.name }} </div>
        
        <input type='text' *ngIf=item.edit [(ngModel)]=item.name (focusout)="editFileName(item)" style="width:100%;"/></li>

    </ul>
    <button type="button" class="btn btn-primary" (click)="newFile()">+</button>
    </div>
    <div
      
      class="app-ace-editor"
      id="app-ace-editor"
      #editor
      style="width: 80%;height: 500px;"
    ></div>
  </div>
<button class="btn btn-icon btn-3 btn-primary btn-lg pull-right" type="button" (click)="run()">
<span class="btn-inner--text">Tester code</span>
</button>
</div>

<div class="container invisible" id="res" >
  <h3 class="mt-lg mb-4">
    <span>Résultats</span>
  </h3>
  <div>
    <ngb-alert [type]="stock.type"  [dismissible]="true"  (close)="close(stock)" >
      <ng-container *ngIf="stock.icon">
        <div class="alert-inner--icon">
            <i class="{{stock.icon}}"></i>
        </div>
      </ng-container>
      <span class="alert-inner--text">  <strong>{{stock.strong}} </strong>{{ stock.message }}</span>
    </ngb-alert>
  </div>
  <div class="container ">
    <div style=" background-color:#282a36 ;">
        <h4 class="mt-lg mb-4">
        <span style=" color:#f1de6d">Bloc retour</span>
      </h4>
      <pre id="retour" class="" style=" color:white ;   max-height : 50vh;overflow: scroll;">{{this.resultPost.stdout}}</pre>
    </div>
    <div style=" background-color:#282a36 ;">
        <h4 class="mt-lg mb-4">
        <span  style=" color:#f1de6d">Bloc erreur</span>
      </h4>
      <pre id="err" class="overflow-scroll"  style=" color:white ;max-height : 50vh;overflow: scroll;">{{this.resultPost.stderr}}</pre>
    </div>
  </div>
</div>


  `,
  styles: [
    `
      .app-ace-editor {
        border: 2px solid #f8f9fa;
        box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
      }
    `,
  ],
})


export class EditeurComponent implements AfterViewInit {
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
    "java":"java"
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
    if(item.edit==false || (item.name.length>0 && verifName.length<2) ){
      item.edit=!item.edit;
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
  }


  public newFile(){
    this.obj.files.push({name : "",content:"dsds",edit:true});
    console.log(this.obj);
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
          document.getElementById("res").className = "container";
          this.stock=this.alerts[this.resultPost.logs.status];
          
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
          type: 'warning',
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
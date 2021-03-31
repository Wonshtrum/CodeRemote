
import { AfterViewInit, Component, ElementRef, Input, ViewChild } from "@angular/core";
import {HttpClient} from '@angular/common/http';
import * as ace from "ace-builds";
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
  <section class="section pb-0 section-components" (oninit)="loadLanguage() ">
  <div class="container mb-5">
  <div class="col-lg-2 col-sm-2">
  <div class="form-group">
    <input type="text" id="name" placeholder="Nom" class="form-control" />
  </div>
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
  <div class="d-flex justify-content-between  ">

    <div>
    <ul>
    <li>Milk</li>
    <li>Cheese
        <ul>
            <li>Blue cheese</li>
            <li>Feta</li>
        </ul>
    </li>
</ul>
    </div>
    <div
      class="app-ace-editor"
      id="app-ace-editor"
      #editor
      style="width: 100%;height: 500px;"
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
      <pre id="retour" class="overflow-scrolls" style=" color:white">
        {{retour}}
      </pre>
    </div>
    <div style=" background-color:#282a36 ;">
        <h4 class="mt-lg mb-4">
        <span  style=" color:#f1de6d">Bloc erreur</span>
      </h4>
      <pre id="err" class="overflow-scroll"  style=" color:white">
        {{error}}
      </pre>
    </div>
  </div>
</div>

</section>
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

  datas ={
    "python3":"python",
    "c++":"c_cpp",
    "c":"c_cpp",
    "php":"php",
    "java":"java"
  }

  stock={}
  lang={}
  // dropDownData= ['python3', 'c++', 'c','php','java','prolog']
  dropDownData ;
  response;
  test = "";
  hash;
  resultPost;
  error;
  retour;

  res_Id_post = 2
  alert: IAlert;

  post={
    "stdout": "string",
    "stderr": "ERRRRRRRERRRRRRRERRRRRRRERRRRRRRERRRRRRRERRRRRRRERRRRRRRERRRRRRRERRRRRRRERRRRRRRERRRRRRRERRRRRRRERRRRRRRERRRRRRRERRRRRRRERRRRRRRERRRRRRRERRRRRRRERRRRRRR",
    "logs": {
      "id":0 ,
      "message": "string",
      "compilation_time": 0.222,
      "execution_time": 0.1111
    }
  }
  public run(){
    var e = (document.getElementById("selectLangage")) as HTMLSelectElement;
    var strLangage = e.options[e.selectedIndex].text;
    var input =  (document.getElementById("name")) as HTMLInputElement;
    console.log(input.value)
    const aceEditor = ace.edit(this.editor.nativeElement);
    console.log(aceEditor.getValue())
    console.log(strLangage);

    const data = {
      lang: strLangage,
      files: [
        {
          name: input.value,
          content: aceEditor.getValue()
        }
      ]
    };
    console.log(data);

    this.http.put('http://127.0.0.1:4382/compile',data)
    .subscribe(response  => {
      this.hash = response
      // If response comes hideloader() function is called
      // to hide that loader 
      console.log(response)

    });
    this.http.post('http://127.0.0.1:4382/result',this.hash)
    .subscribe(response  => {
      this.resultPost=response
      // If response comes hideloader() function is called
      // to hide that loader 
      console.log(response)

    });



    // axios post renvoie res succes avec le texte
    document.getElementById("res").className = "container";
    this.stock=this.alerts[this.post.logs.id];
    // let content_retour = document.createTextNode(this.post.stdout);
    // let content_err = document.createTextNode(this.post.stderr);
    // document.getElementById("retour").appendChild(content_retour);
    // document.getElementById("err").appendChild(content_err);
    this.retour=this.post.stdout
    this.error=this.post.stderr
    
  }

  public onOptionsSelected(event) {
    console.log(event);
    const aceEditor = ace.edit(this.editor.nativeElement);
    aceEditor.session.setMode("ace/mode/"+event);
  }
  @ViewChild("editor") private editor: ElementRef<HTMLElement>;


  ngOnInit(){

    
    this.http.get('http://127.0.0.1:4382/languages')
    .subscribe(response  => {
  
      // If response comes hideloader() function is called
      // to hide that loader 
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
    aceEditor.session.setValue("toto=\"Welcome to our compilator\" ");
    aceEditor.setTheme("ace/theme/dracula");
    aceEditor.session.setMode("ace/mode/python");
    aceEditor.on("change", () => {
      console.log(aceEditor.getValue());
      this.test= aceEditor.getValue();
      console.log(this.test)
    });
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
          strong: 'Info!',
          type: 'info',
          message: 'La compilation est en cours !',
          icon: 'ni ni-bell-55'
      }, {
          id: 2,
          type: 'warning',
          strong: 'Warning!',
          message: 'La compilation met trop de temps à s\'éxécuter !',
          icon: 'ni ni-bell-55'
      }, {
          id: 3,
          type: 'danger',
          strong: 'Danger!',
          message: 'La compilation a échoué!',
          icon: 'ni ni-support-16'
      });
      this.backup = this.alerts.map((alert: IAlert) => Object.assign({}, alert));
  }

  close(alert: IAlert) {
    this.alerts.splice(this.alerts.indexOf(alert), 1);
  }
}
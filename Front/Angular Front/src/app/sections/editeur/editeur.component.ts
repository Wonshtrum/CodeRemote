
import { AfterViewInit, Component, ElementRef, ViewChild } from "@angular/core";
import * as ace from "ace-builds";

@Component({
  selector: "app-editeur",
  template: `
  <section class="section pb-0 section-components">
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
   [value]="data[option] || 'text'">{{option}}</option>
</select>
  </div>
  </div>
 
    <div
      class="app-ace-editor"
      id="app-ace-editor"
      #editor
      style="width: 100%;height: 500px;"
    ></div>

<button class="btn btn-icon btn-3 btn-primary btn-lg pull-right" type="button" (click)="run()">
<span class="btn-inner--text">Tester code</span>
</button>
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

  data ={
    "python3":"python",
    "c++":"c_cpp",
    "c":"c_cpp",
    "php":"php",
    "java":"java"
  }

    
  dropDownData= ['python3', 'c++', 'c','php','java','prolog']





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
    return(data);
  }

  public onOptionsSelected(event) {
    console.log(event);
    const aceEditor = ace.edit(this.editor.nativeElement);
    aceEditor.session.setMode("ace/mode/"+event);
  }
  @ViewChild("editor") private editor: ElementRef<HTMLElement>;

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
    });
  }
}
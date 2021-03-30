
import { AfterViewInit, Component, ElementRef, ViewChild } from "@angular/core";
import * as ace from "ace-builds";

@Component({
  selector: "app-root",
  template: `
  <input type="text" id="name">
    <div
      class="app-ace-editor"
      id="app-ace-editor"
      #editor
      style="width: 500px;height: 250px;"
    ></div>
    <select class='select-option'
    id ="selectLangage"
    #mySelect
    (change)='onOptionsSelected(mySelect.value)'>
   <option class='option' 
   *ngFor='let option of dropDownData' 
   [value]="option">{{option}}</option>
</select>
<button class="btn btn-icon btn-3 btn-primary" type="button" (click)="run()">
<span class="btn-inner--text">Tester code</span>
</button>

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
export class AppComponent implements AfterViewInit {
  dropDownData = ["python","html","java"];


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
    aceEditor.setTheme("ace/theme/twilight");
    aceEditor.session.setMode("ace/mode/python");
    aceEditor.on("change", () => {
      console.log(aceEditor.getValue());
    });
  }
}
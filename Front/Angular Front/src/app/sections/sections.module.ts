import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { FormsModule } from '@angular/forms';
import { NouisliderModule } from 'ng2-nouislider';
import { JwBootstrapSwitchNg2Module } from 'jw-bootstrap-switch-ng2';
import { RouterModule } from '@angular/router';

import { SectionsComponent } from './sections.component';
import { ButtonsSectionComponent } from './buttons-section/buttons-section.component';
import { InputsSectionComponent } from './inputs-section/inputs-section.component';

import { AlertsSectionComponent } from './alerts-section/alerts-section.component';
import { EditeurComponent } from './editeur/editeur.component';



@NgModule({
  declarations: [
    SectionsComponent,
    ButtonsSectionComponent,
    InputsSectionComponent,

    AlertsSectionComponent,

    EditeurComponent



  ],

  imports: [
    CommonModule,
    FormsModule,
    NgbModule,
    RouterModule,
    NouisliderModule,
    JwBootstrapSwitchNg2Module
  ],
  exports:[ SectionsComponent ]
})
export class SectionsModule { }

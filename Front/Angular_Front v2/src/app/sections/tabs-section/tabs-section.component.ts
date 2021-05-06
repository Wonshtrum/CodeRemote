import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-tabs-section',
  templateUrl: './tabs-section.component.html',
  styleUrls: ['./tabs-section.component.css']
})
export class TabsSectionComponent implements OnInit {
  page = 2;
  page1 = 3;

  codePython_1=`
  from test import hello
  print(hello())
  `
  codePython_2=`
  def hello():
    toto = "Bonjour"
    tata = " compilateur!"
    return(toto+tata)
  `


  codeC_1=`
  #ifndef __TEST_H__
  #define __TEST_H__
  #include <iostream>
  void test();
  #endif
  `
  codeC_2=`
  #include "test.h"

  void test() {
    std::cout << "Test succesfull!" << std::endl;
  }
  `

  codeC_3=`
  #include "test.h"

  int main(void) {
    test();
    return 0;
  }
  `

  constructor() { }

  ngOnInit() {
  }

}

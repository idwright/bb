import { Component, EventEmitter, Input, Output, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';

@Component({
  selector: '[app-property-form]',
  templateUrl: './property-form.component.html',
  styleUrls: ['./property-form.component.css']
})
export class PropertyFormComponent implements OnInit {

  @Input('group')
  public pForm: FormGroup;
  
  @Input('index')
  public index: number;

  public userEditable: boolean = false;

  @Output()
  public removed: EventEmitter<number> = new EventEmitter<number>();

  ngOnInit(): void {
    if (this.pForm.controls["source"].value == 'backbone') {
      this.userEditable = true;
    }
  }
  static initProperty(source, data_name, data_value, data_type) {
    
    let prop = new FormGroup({
      source: new FormControl( source, Validators.required),
      data_name: new FormControl( data_name, Validators.required),
      data_value: new FormControl( data_value),
      data_type: new FormControl(data_type)
    });
    
    return prop;
  }
}

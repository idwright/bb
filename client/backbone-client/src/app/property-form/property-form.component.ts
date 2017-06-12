import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';

@Component({
  selector: '[app-property-form]',
  templateUrl: './property-form.component.html',
  styleUrls: ['./property-form.component.css']
})
export class PropertyFormComponent {

  @Input('group')
  public pForm: FormGroup;
  
  @Input('index')
  public index: number;

  @Output()
  public removed: EventEmitter<number> = new EventEmitter<number>();
  
  static initProperty(source, data_name, data_value, data_type) {
    return new FormGroup({
      source: new FormControl(source, Validators.required),
      data_name: new FormControl(data_name, Validators.required),
      data_value: new FormControl(data_value),
      data_type: new FormControl(data_type)
    });
  }
}

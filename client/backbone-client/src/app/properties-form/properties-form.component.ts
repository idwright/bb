import { Component, Input } from '@angular/core';
import { FormArray } from '@angular/forms';

import { Property } from '../typescript-angular2-client/model/Property';

import { PropertyFormComponent } from '../property-form/property-form.component';

@Component({
  selector: 'app-properties-form',
  templateUrl: './properties-form.component.html',
  styleUrls: ['./properties-form.component.css']
})
export class PropertiesFormComponent {

  @Input('properties')
  public properties: FormArray;

  removeProperty(i: number) {
    this.properties.removeAt(i);
  }
  
  static initValues(values) {
    let valuesArray = new FormArray([]);
    values.forEach(prop => {
      let propControl = PropertyFormComponent.initProperty(prop.source, prop.data_name, prop.data_value, prop.data_type);
      valuesArray.push(propControl);
    });
    return valuesArray;
  }

  addProperty() {
    this.properties.push(PropertyFormComponent.initProperty('backbone', '', '', Property.DataTypeEnum.String));
  }
}

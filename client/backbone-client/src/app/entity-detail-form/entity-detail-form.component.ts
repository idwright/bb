import 'rxjs/add/operator/switchMap';
import { Component, Input, OnInit, ViewEncapsulation } from '@angular/core';
import { FormGroup, FormArray, FormControl, FormBuilder, Validators } from '@angular/forms';
import { ActivatedRoute, Params } from '@angular/router';
import { Location } from '@angular/common';

import { Entity } from '../typescript-angular2-client/model/Entity';
import { Property } from '../typescript-angular2-client/model/Property';
import { EntityApi } from '../typescript-angular2-client/api/EntityApi';
@Component({
  selector: 'entity-detail-form',
  templateUrl: './entity-detail-form.component.html',
  styleUrls: [
    './entity-detail-form.component.css'
  ],
  encapsulation: ViewEncapsulation.None,
})
export class EntityDetailFormComponent implements OnInit {

  @Input() entity: Entity;

  public entityForm: FormGroup;
  constructor(
    private entityService: EntityApi,
    private route: ActivatedRoute,
    private location: Location,
    private _fb: FormBuilder
  ) { }

  ngOnInit(): void {
    this.route.params
      .switchMap((params: Params) => this.entityService.downloadEntity(params['entityId']))
      .subscribe(response => {
        this.entity = response;

        this.entityForm = this._fb.group({
          entity_id: [this.entity.entity_id, [Validators.required, Validators.minLength(5)]],
          values: this._fb.array([]),
          refs: this._fb.array([]),
        });
        const control = <FormArray>this.entityForm.controls['values'];
        this.initValues(control, this.entity.values);

        this.entity.refs.forEach(ref => {
          let propControl = this.initAssoc(ref.assoc_name, ref.source_id, ref.target_id, '');
          this.pushAssoc(propControl);
          this.initValues(propControl, ref.values);
        })
      });
  }

  initValues(parentControl, values) {
    values.forEach(prop => {
      let propControl = this.initProperty(prop.source, prop.data_name, prop.data_value, prop.data_type);
      parentControl.push(propControl);
    });
  }
  initProperty(source, data_name, data_value, data_type) {
    return this._fb.group({
      source: [source, Validators.required],
      data_name: [data_name, [Validators.required, Validators.minLength(3)]],
      data_value: [data_value ],
      data_type: [data_type]
    });
  }

  pushProperty(propControl) {
    const control = <FormArray>this.entityForm.controls['values'];
    control.push(propControl);
  }
  addProperty() {
    this.pushProperty(this.initProperty('backbone', '', '', Property.DataTypeEnum.String));
  }

  removeProperty(i: number) {
    const control = <FormArray>this.entityForm.controls['values'];
    control.removeAt(i);
  }

  initAssoc(assoc_name, source_id, target_id, assoc_type) {
    return this._fb.group({
      assoc_name: [assoc_name, Validators.required],
      source_id: [source_id],
      target_id: [target_id],
      values: this._fb.array([]),
    });
  }

  pushAssoc(propControl) {
    const control = <FormArray>this.entityForm.controls['refs'];
    control.push(propControl);
  }

  removeAssoc(i: number) {
    const control = <FormArray>this.entityForm.controls['refs'];
    control.removeAt(i);
  }
  goBack(): void {
    this.location.back();
  }

  public onSubmit(): void {

    console.log("Submitting:" + JSON.stringify(this.entity));
    this.entityService.updateEntity(this.entity.entity_id, this.entity)
      .subscribe(
      (x) => {
        console.log("Submitted");
      },
      (e) => { console.log('onError: %o', e); },
      () => {
        console.log('Completed update.');
      }
      );
  }

  private onFormChange() {
    console.log("Changing:" + this.entity.entity_id);
  }

}


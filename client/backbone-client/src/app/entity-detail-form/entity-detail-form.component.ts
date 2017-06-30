import 'rxjs/add/operator/switchMap';
import { Component, Input, OnInit, ViewEncapsulation } from '@angular/core';
import { FormGroup, FormArray, FormControl, FormBuilder, Validators } from '@angular/forms';
import { ActivatedRoute, Params } from '@angular/router';
import { Location } from '@angular/common';

import { Entity } from '../typescript-angular2-client/model/Entity';
import { Property } from '../typescript-angular2-client/model/Property';
import { EntityApi } from '../typescript-angular2-client/api/EntityApi';

import { PropertiesFormComponent } from '../properties-form/properties-form.component';

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

        let entityValues = PropertiesFormComponent.initValues(this.entity.values);
        this.entityForm = this._fb.group({
          entity_id: [this.entity.entity_id, [Validators.required, Validators.minLength(5)]],
          values: entityValues,
          refs: this._fb.array([]),
        });



        this.entity.refs.forEach(ref => {
          let refValues = PropertiesFormComponent.initValues(ref.values);
          let propControl = this.initAssoc(ref.assoc_name, ref.source_id, ref.target_id, '', refValues);
          this.pushAssoc(propControl);
          console.log(propControl);
        })
      });
  }

  initAssoc(assoc_name, source_id, target_id, assoc_type, refValues) {
    return new FormGroup({
      assoc_name: new FormControl(assoc_name, Validators.required),
      source_id: new FormControl(source_id, Validators.required),
      target_id: new FormControl(target_id, Validators.required),
      values: refValues,
    });
  }

  pushAssoc(propControl) {
    const control = <FormArray>this.entityForm.controls['refs'];
    control.push(propControl);
  }

  goBack(): void {
    this.location.back();
  }

  public onSubmit({ value, valid }: { value: Entity, valid: boolean }): void {

    console.log("Submitting:" + JSON.stringify(value));
    this.entityService.updateEntity(value.entity_id, value)
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

  addAssociation() {
    let aValues = PropertiesFormComponent.initValues([]);

    let propControl = this.initAssoc('', '', '', '', aValues);
    this.pushAssoc(propControl);
  }
  private onFormChange() {
    console.log("Changing:" + this.entity.entity_id);
  }

}


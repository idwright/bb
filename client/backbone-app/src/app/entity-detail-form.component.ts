import 'rxjs/add/operator/switchMap';
import { Component, Input, OnInit }      from '@angular/core';
import { FormGroup } from '@angular/forms';
import { ActivatedRoute, Params } from '@angular/router';
import { Location }               from '@angular/common';

import { Entity } from './typescript-angular2-client/model/Entity';
import { EntityApi }          from './typescript-angular2-client/api/EntityApi';
@Component({
  selector: 'entity-detail-form',
  templateUrl: './entity-detail-form.component.html',
  styleUrls: [ './entity-detail-form.component.css' ]
})
export class EntityDetailFormComponent implements OnInit {
  @Input() entity: Entity;

  form: FormGroup;
  constructor(
    private entityService: EntityApi,
    private route: ActivatedRoute,
    private location: Location
  ) {}

  ngOnInit(): void {
    this.route.params
      .switchMap((params: Params) => this.entityService.downloadEntity(params['entity_id']))
      .subscribe(response => this.entity = response);
  }

  goBack(): void {
    this.location.back();
  }

  public onSubmit(): void {

    console.log("Submitting:" + this.entity);
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


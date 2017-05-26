import 'rxjs/add/operator/switchMap';
import { Component, Input, OnInit }      from '@angular/core';
import { FormGroup } from '@angular/forms';
import { ActivatedRoute, Params } from '@angular/router';
import { Location }               from '@angular/common';

import { Entity } from './typescript-angular2-client/model/Entity';
import { EntityApi }          from './typescript-angular2-client/api/EntityApi';
@Component({
  selector: 'entity-detail',
  template: '<entity-detail-form></entity-detail-form>',
  styleUrls: [ './entity-detail.component.css' ]
})
export class EntityDetailComponent {

}


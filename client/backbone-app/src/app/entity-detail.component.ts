import 'rxjs/add/operator/switchMap';
import { Component, OnInit }      from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Location }               from '@angular/common';

import { Entity } from './typescript-angular2-client/model/Entity';
import { EntityApi }          from './typescript-angular2-client/api/EntityApi';
@Component({
  selector: 'entity-detail',
  templateUrl: './entity-detail.component.html',
  styleUrls: [ './entity-detail.component.css' ]
})
export class EntityDetailComponent implements OnInit {
  entity: Entity;

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
}


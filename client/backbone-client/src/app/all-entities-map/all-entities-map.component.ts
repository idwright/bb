import { Component, OnInit } from '@angular/core';
import { QueryEncoder } from '@angular/http';

import { Entities } from '../typescript-angular2-client/model/Entities';
import { Entity } from '../typescript-angular2-client/model/Entity';
import { Property } from '../typescript-angular2-client/model/Property';

import { EntityApi } from '../typescript-angular2-client/api/EntityApi';
import { Summary } from '../typescript-angular2-client/model/Summary';

@Component({
  selector: 'app-all-entities-map',
  providers: [EntityApi],
  templateUrl: './all-entities-map.component.html',
  styleUrls: ['./all-entities-map.component.css']
})
export class AllEntitiesMapComponent implements OnInit {

  entities: Entities;

  constructor(private entityApi: EntityApi) { }


  ngOnInit() {
    this.loadEntities();
  }

  loadEntities(): void {
    let coder = new QueryEncoder();
    this.entityApi.downloadEntitiesByProperty('latitude', coder.encodeValue('*')).subscribe(
      (entities) => { 
        this.entities = entities
        console.log(this.entities);
      },
      (err) => console.log(err),
      () => { console.log("Downloaded entities") }
    );
  }

}

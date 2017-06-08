import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Location }               from '@angular/common';

import { Entities } from '../typescript-angular2-client/model/Entities';

import { EntityApi } from '../typescript-angular2-client/api/EntityApi';

@Component({
  selector: 'entities-list',
  templateUrl: './entities-list.component.html',
  styleUrls: [ './entities-list.component.css' ]
})
export class EntitiesListComponent implements OnInit {

    entities: Entities;

    sourceName: string;

    propertyName: string;
    propertyValue: string;

    constructor(private entityApi: EntityApi,
              private route: ActivatedRoute,
              private location: Location
              ) { 
    }

    ngOnInit(): void {
        this.sourceName = this.route.snapshot.params['sourceId'];
        this.propertyName = this.route.snapshot.params['propertyName'];
        this.propertyValue = this.route.snapshot.params['propertyValue'];

        console.log("entities list:" + this.sourceName + "/" + this.propertyName);
    }


    goBack(): void {
      this.location.back();
    }

}

import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Location }               from '@angular/common';

import { Entities } from './typescript-angular2-client/model/Entities';

import { EntityApi } from './typescript-angular2-client/api/EntityApi';

@Component({
  selector: 'entities-list',
  templateUrl: './entities-list.component.html',
  styleUrls: [ './entities-list.component.css' ]
})
export class EntitiesListComponent implements OnInit {

    entities: Entities;

    sourceName: string;

    propertyName: string;

    constructor(private entityApi: EntityApi
              private route: ActivatedRoute,
              private location: Location
              ) { 
    }

    ngOnInit(): void {
        this.sourceName = this.route.snapshot.params['sourceId'];
        this.propertyName = this.route.snapshot.params['propertyName'];

        console.log("entities list:" + this.sourceName + "/" + this.propertyName);

        this.sourceName = this.route.snapshot.params['sourceId'];

      this.route.params.switchMap((params: Params) =>
        this.entityApi.downloadEntitiesByProperty(params['propertyName'], params['propertyValue'])).subscribe(
            (entities) => {
                            console.log(entities);
                            this.entities = entities;
                        },
                        (err) => console.log(err),
                        () => { console.log("Downloaded entities") }
        );

    }


    goBack(): void {
      this.location.back();
    }

}

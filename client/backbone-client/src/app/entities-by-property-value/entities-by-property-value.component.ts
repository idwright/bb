import { Component, OnInit } from '@angular/core';

import { ActivatedRoute, Params } from '@angular/router';

@Component({
  selector: 'app-entities-by-property-value',
  templateUrl: './entities-by-property-value.component.html',
  styleUrls: ['./entities-by-property-value.component.css']
})
export class EntitiesByPropertyValueComponent implements OnInit {

  propertyName: string;
  propertyValue: string;

  constructor(private route: ActivatedRoute) {
  }

  ngOnInit() {

    this.propertyName = this.route.snapshot.params['propertyName'];
    this.propertyValue = this.route.snapshot.params['propertyValue'];

  }
}

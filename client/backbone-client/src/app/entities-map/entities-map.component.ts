import { Component, OnInit, Input } from '@angular/core';

import { Entities } from '../typescript-angular2-client/model/Entities';
import { Entity } from '../typescript-angular2-client/model/Entity';
import { Property } from '../typescript-angular2-client/model/Property';

import * as L from 'leaflet';

@Component({
  selector: 'app-entities-map',
  templateUrl: './entities-map.component.html',
  styleUrls: ['./entities-map.component.css']
})
export class EntitiesMapComponent implements OnInit {


  _entities: Entities;

  leaflet_options;

  leaflet_layers_control;

  markers: L.Layer[] = [];

  constructor() { }

  @Input()
  set entities(entities: Entities) {
    this._entities = entities;
    //console.log(this._entities);
    if (entities) {
      entities.entities.forEach(entity => {
        let entityRow: any = {
          'entityId': entity.entity_id,
          'refs': entity.refs.length
        };
        let lat: number = null;
        let lng: number = null;
        let loc: string = '';
        entity.values.forEach(prop => {
          if (prop.data_name == 'latitude') {
            lat = Number(prop.data_value);
          }
          if (prop.data_name == 'longitude') {
            lng = Number(prop.data_value);
          }
          if (prop.data_name == 'location') {
            loc = prop.data_value;
          }
        });
        if (lat && lng) {
          this.addMarker(lat, lng, loc);
        }
      });
    }
  }

  ngOnInit() {
    this.leaflet_options = {
      layers: [
        L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18, attribution: '...' })
      ],
      zoom: 3,
      center: L.latLng([-4.6991, 20.8422])
    };

    this.leaflet_layers_control = {
      baseLayers: {
        'Open Street Map': L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18, attribution: '...' })
      }
    }

    console.log(this._entities);

    //this.addMarker();
  }

  addMarker(lat, lng, marker_title) {
    let marker = L.marker(
      [lat, lng],      
      {
        title: marker_title,        
        icon: L.icon({
          iconSize: [25 * 0.5, 41 * 0.5],
          iconAnchor: [13 * 0.5, 0 ],
          iconUrl: 'assets/marker-icon.png',
          shadowUrl: 'assets/marker-shadow.png'
        })
      }
    );

    this.markers.push(marker);
  }
}

import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EntitiesMapComponent } from './entities-map.component';

describe('EntitiesMapComponent', () => {
  let component: EntitiesMapComponent;
  let fixture: ComponentFixture<EntitiesMapComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EntitiesMapComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EntitiesMapComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});

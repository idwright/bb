import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AllEntitiesMapComponent } from './all-entities-map.component';

describe('AllEntitiesMapComponent', () => {
  let component: AllEntitiesMapComponent;
  let fixture: ComponentFixture<AllEntitiesMapComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AllEntitiesMapComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AllEntitiesMapComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});

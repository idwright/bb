import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EntitiesByPropertyValueComponent } from './entities-by-property-value.component';

describe('EntitiesByPropertyValueComponent', () => {
  let component: EntitiesByPropertyValueComponent;
  let fixture: ComponentFixture<EntitiesByPropertyValueComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EntitiesByPropertyValueComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EntitiesByPropertyValueComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});

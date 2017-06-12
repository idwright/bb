import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PropertiesFormComponent } from './properties-form.component';

describe('PropertiesFormComponent', () => {
  let component: PropertiesFormComponent;
  let fixture: ComponentFixture<PropertiesFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PropertiesFormComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PropertiesFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});

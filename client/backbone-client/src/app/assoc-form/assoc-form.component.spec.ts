import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AssocFormComponent } from './assoc-form.component';

describe('AssocFormComponent', () => {
  let component: AssocFormComponent;
  let fixture: ComponentFixture<AssocFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AssocFormComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AssocFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});

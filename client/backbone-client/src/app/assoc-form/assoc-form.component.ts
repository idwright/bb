import { Component, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';
@Component({
  selector: 'app-assoc-form',
  templateUrl: './assoc-form.component.html',
  styleUrls: ['./assoc-form.component.css']
})
export class AssocFormComponent {

  @Input('group')

  public aForm: FormGroup;
}

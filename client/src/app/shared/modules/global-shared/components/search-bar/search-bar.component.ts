import { Component, OnInit, Input } from '@angular/core';
import { FormControl } from '@angular/forms';
import { map, startWith } from 'rxjs/operators';
import { Observable } from 'rxjs';
@Component({
  selector: 'app-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.scss']
})
export class SearchBarComponent implements OnInit {

  myControl = new FormControl();
  filteredOptions: Observable<string[]>;
  options: any[] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p'];

  @Input() searchbarWidth: number;
  @Input() searchbarHeight: number;

  constructor() { }

  ngOnInit() {
    this.filteredOptions = this.myControl.valueChanges
      .pipe(
        startWith(''),
        map(value => this.filter(value))
      );
  }

  private filter(value: string): string[] {
    const filterValue = value.toLowerCase();
    return this.options.filter(option => option.toLowerCase().includes(filterValue));
  }

  autoCompleteOpen(event) {
    $('.search-bar-wrapper').css('border-radius', `${this.searchbarHeight / 2}px ${this.searchbarHeight / 2}px 0 0`);
    $('.search-auto-complete').css('border-radius', `0 0 ${this.searchbarHeight / 2}px ${this.searchbarHeight / 2}px`);
    $('.search-auto-complete').css('max-height', this.searchbarHeight * 5);
    $('.search-auto-complete').css('width', `${this.searchbarWidth}`);
    $('.cdk-overlay-pane').css('width', `${this.searchbarWidth}`);
    $('.cdk-overlay-pane').css('tranform', `translateX(${this.searchbarHeight + 12}px)`);
  }

  autoCompleteClosed(event) {
    $('.search-bar-wrapper').css('border-radius', `${this.searchbarHeight / 2}px`);
  }

}

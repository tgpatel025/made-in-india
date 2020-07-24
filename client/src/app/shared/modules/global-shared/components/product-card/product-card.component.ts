import { Component, OnInit, Input } from '@angular/core';
import { MatChip, MatChipList } from '@angular/material/chips';
import { ProductDetailsModel } from 'src/app/shared/models/product-details.model';

@Component({
  selector: 'app-product-card',
  templateUrl: './product-card.component.html',
  styleUrls: ['./product-card.component.scss']
})
export class ProductCardComponent implements OnInit {


  @Input() productDetails: ProductDetailsModel;

  constructor() { }

  ngOnInit(): void {
  }

  goToFlipkart() {
    window.open(this.productDetails.Product_Link);
  }

  openDetails() {
    window.alert('coming soon...');
  }

}

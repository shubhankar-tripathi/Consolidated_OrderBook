import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup} from "@angular/forms";
import {AppServiceService} from '../app-service.service';

@Component({
  selector: 'app-snapshot',
  templateUrl: './snapshot.component.html',
  styleUrls: ['./snapshot.component.css']
})
export class SnapshotComponent implements OnInit {
  rForm: FormGroup;
  post:any;                     // A property for our submitted form
  data: any = [];
  price:string = '0';
  default: string = '';
  titleAlert:string = 'This field is required';
  exchange: string = 'Both';
  exchangeList: string[] = ['GDAX', 'Bitfinex', 'Both'];

  constructor(private fb:FormBuilder,private appService: AppServiceService) {
    this.rForm = fb.group({
      'price': [null],
      'exchange' : [this.exchangeList],
    });
    setInterval(() => {

      this.appService.getCustomOrderBook(this.price, this.exchange).subscribe(data => this.data = data);
    }, 400);
  }

  ngOnInit() {

  }

  addPost(post) {
    console.log(post);
    this.price = post.price;
    this.exchange = post.exchange;
    console.log(this.price + " " + this.exchange);
  }

}
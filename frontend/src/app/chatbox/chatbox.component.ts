import { Component, OnInit, ViewChild, ElementRef} from '@angular/core';
import { Message } from '../models/message.model';
import { MESSAGES } from '../models/mock-messages';
import { ChatboxService } from '../chatbox.service';

@Component({
  selector: 'app-chatbox',
  templateUrl: './chatbox.component.html',
  styleUrls: ['./chatbox.component.css']
})
export class ChatboxComponent implements OnInit {
  @ViewChild('myDiv') myDiv: ElementRef;

  triggerFalseClick() {
    let el: HTMLElement = this.myDiv.nativeElement as HTMLElement;
    el.click();
  }
  check:boolean = false;
  sentiment: number;
  
  messages : Message[] = [];
  constructor(private chatService: ChatboxService) { }
  ngOnInit() {
    let message = new Message("Welcome to my chatbot", "assets/assets/images/bot.png");
    this.messages.push(message);
  }
  sendMessage(message_content){
    if(message_content.value != ""){
      let message = new Message(message_content.value, "assets/assets/images/user.png");
      this.messages.push(message);
    
      this.chatService.sendMessage(message_content.value).subscribe((res:any) => {
        let message = new Message(res.result.speech, "assets/assets/images/bot.png");
        this.messages.push(message);
        console.log(res);
        message_content.value = "";
      }, err =>{
        console.log(err);
      })
    }
  }
  consoledot(message_content){
    this.chatService.getEmotion(message_content.value).subscribe((res: any) => {
      this.sentiment = res.sentiment;
      console.log(res);
      this.check = (res.sentiment === 1);
    }, err => {
      console.log(err);
    })
  }
}

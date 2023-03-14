import React from "react";
import Sec from "./Sec";
import Sec1 from "./Sec1";
import Sec2 from "./Sec2";
import "./Header.css"
import Dropdown from "./Dropdown";
import { useState } from "react";
import Calendar from 'react-calendar';
import {BiFullscreen,FiMinimize} from "react-icons/all"
// import 'react-calendar/dist/Calendar.css';
// import 'bootstrap/dist/css/bootstrap.min.css';
const Homepage = () => {
  const [date, setDate] = useState(new Date());
  const [selected, setSelected] = useState("Choose One");
  const [t1,setT1]=useState(false)

  const handlet=()=>{
    setT1(true)
  }
  return (
    <div className="homepage">
      <div className="home">
        <div className="head">
          <div className="heading">
            <div className="head1">HEALTHCARE SEC</div>
            <div className="head2">CAMSEC.AI</div>
          </div>
        </div>

        <hr id="hr"/>
      </div>
      {t1===false?
      <div>
      <div className="homecontent"style={{marginLeft:'6vh',marginTop:'1vh'}}>
        <div className="data1">
          <div className="secbar">
            <Sec />
            <Sec1 />
            <Sec2 />
            {/* <Sec />
            <Sec />
            <Sec />
            <Sec />
            <Sec /> */}
          </div>
          <div className="cams">
            <div className="camheader y">
              <div style={{marginLeft:'3vh'}}>Cameras</div>
              <div className="y">
                <p className="full" style={{marginLeft:'68vh'}}>Full Screen</p>
                  <BiFullscreen 
                  onClick={()=>handlet()} className='ght'/>
              </div>
            </div>
            <div className="homecams">
              <div className="democam">1</div>
              <div className="democam">2</div>
              <div className="democam">3</div>
              <div className="democam">4</div>
            </div>
          </div>
        </div>
        <div className=""style={{marginTop:'1.6%',marginLeft:'4%'}}>
          <div className="all-games">
          <div className="react-calendar">
          <Calendar onChange={setDate}
          value={date} 
          />
        </div>
        </div>
          {/* <h1 className='text-center'>React Calendar with Range</h1> */}
          <div className="graph" >
            <b style={{display:'flex',justifyContent:'center',color:'#b2bec3'
             ,marginTop:'5%'}}>Activity</b>
            <div style={{display:'flex',flexDirection:'roe',marginTop:'10%'
             ,marginLeft:'10%'}}>
            <div style={{borderRight:'12px solid #b2bec3',width:'12px'
             ,height:'23.4vh',
              marginTop:'22%',borderTopRightRadius:'15px',
              borderTopLeftRadius:'15px'}}>      
            </div>
            <div style={{borderRight:'12px solid #b2bec3',
              marginLeft:'11%',width:'12px'
            ,height:'20vh',marginTop:'30.5%'}}>       
           </div> 
           <div style={{borderRight:'12px solid #b2bec3',marginLeft:'11%'
            ,width:'12px'
            ,height:'27vh',marginTop:'13%'}}>       
           </div>
            <div style={{borderRight:'12px solid #b2bec3',marginLeft:'11%'
            ,width:'12px',height:'21.4vh',marginTop:'27%'}}>       
           </div>
            <div style={{borderRight:'12px solid #b2bec3',
             marginLeft:'11%',width:'12px',height:'30vh',marginTop:'6%'}}>       
           </div>
           <div style={{borderRight:'12px solid #b2bec3',marginLeft:'11%'
            ,width:'12px',height:'18.6vh',marginTop:'35%'}}>       
           </div> 
           <div style={{borderRight:'12px solid #b2bec3',marginLeft:'11%'
            ,width:'12px',height:'14vh',marginTop:'47%'}}>       
           </div> 
           </div>
           <div style={{display:'flex',flexDirection:'row',marginLeft:'9%'}}>
                <b style={{display:'flex',justifyContent:'center',color:'#b2bec3'
                  ,marginTop:'7%'}}>Mon</b>
                <b style={{display:'flex',justifyContent:'center',marginLeft:'6%'
                  ,color:'#b2bec3',marginTop:'7%'}}>Tue</b>
                <b style={{display:'flex',justifyContent:'center',marginLeft:'6%'
                  ,color:'#b2bec3',marginTop:'7%'}}>Wed</b>
                <b style={{display:'flex',justifyContent:'center',marginLeft:'6%'
                  ,color:'#b2bec3',marginTop:'7%'}}>Thu</b>
                <b style={{display:'flex',justifyContent:'center',marginLeft:'6%'
                  ,color:'#b2bec3',marginTop:'7%'}}>Fri</b>
                <b style={{display:'flex',justifyContent:'center',marginLeft:'9%'
                  ,color:'#b2bec3',marginTop:'7%'}}>Sat</b>
                <b style={{display:'flex',justifyContent:'center',marginLeft:'8%'
                  ,color:'#b2bec3',marginTop:'7%'}}>Son</b>
             </div>
          </div>
        </div>
      </div>
      </div>:<div className="cams1">
            <div className="camheader y" style={{marginTop:'2vh'}}>
              <div style={{marginLeft:'8vh',color:'white'}}>Cameras</div>
              <div className="y">
                <b className='full' style={{marginLeft:'117vh'}}>Minimize</b>
                <FiMinimize  onClick={()=>setT1(false)} className='ght' />
              </div>
            </div>
            <div className="homecams">
              {/* <div className="democam">1</div>
              <div className="democam">2</div>
              <div className="democam">3</div>
              <div className="democam">4</div> */}
            </div>
          </div>
        }
    </div>
  );
};

export default Homepage;

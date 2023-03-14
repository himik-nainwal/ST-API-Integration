import React, { useState,useEffect } from "react";
import Camselection from "./Cameraselection";
import Ipname from "./Ipname/Ipname";
import Name from "./Name/Name";
import Assign from "./Assign/Assign";
import Type from "./Type/Type";
import Authority from "./Authority/Authority";
import Settingcard from "./Settingcard";
import {AiOutlineDownload} from "react-icons/all"
import { MDBCard, MDBCardBody, MDBCardTitle } from "mdb-react-ui-kit";
import Assigndropdown from "./Assign/Assigndropdown";
import Authoritydropdown from "./Authority/Authoritydropdown";
import Stack from '@mui/material/Stack';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';
import { DeleteOutline, PausePresentationTwoTone, SentimentVerySatisfiedSharp, ShowChart, UpdateOutlined } from '@material-ui/icons';
import axios from "axios"
const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});
import Dropdown from "../Dropdown";
const Camerasetting = () => {
  const [name,setName]=useState('')
  const [rtsp,setRtsp]=useState('')
  const [ip,setIp]=useState('')
  const [authority,setAuthority]=useState('')
  const [assign,setAssign]=useState('')
  const [cam,setCamse]=useState('')
  const [selected, setSelected] = useState("Choose One");
  const [selected1, setSelected1] = useState("Choose One");
  const [state1, setState1] = React.useState({
    open: false,
    open2:false,
    vertical: 'top',
    horizontal: 'right',
  });
  const [open3, setOpen] = React.useState(true);
  const [open1, setOpen1] = React.useState(true);
  const [view,setView]= useState("")
  const [daa,setDaa]=useState([])
  const [view1,setView1]=useState("")
  const [n,setN]=useState('')
  const [message,setMessage]=useState('')
  const { vertical, horizontal, open } = state1;
  const [data,setdata]=useState([])
  var c=data.type
  const [selected2, setSelected2] = useState("Choose One");
  console.log("ssssssssssssssssssssssssssssssssssss",c)
  useEffect(function () {
    getCamera()
    }, []); 
 const getCamera=()=>{
   axios.get("http://127.0.0.1:5000/getcamera") 
   .then((user) => {
     setDaa(user.data)
   })
 } 
 console.log("",daa)
 const handleClose = () => {
  setState1({ ...state1, open: false });
};
  const handle=async()=>{
    var body={
      rtsp:rtsp,
      name:name,
      ip:ip,
      model:selected1,
      type:selected2,
     }
    
    console.log(body)
    try {
        const response = await fetch(`http://127.0.0.1:5000/add`, {
          // const response = await fetch(`http://localhost:5000/companyroutes/addcamera`, {
          method: "POST",
          mode: "cors",
          headers: { "Content-Type": "application/json;charset=utf-8" },
          body: JSON.stringify(body),
        });
        const result = await response.json();
        console.log("ddddddddddd",result)
        setMessage(result)
        setState1({open:true,vertical: 'top',
        horizontal: 'right'})
        getCamera()
        return result;
      } catch (e) {
        console.log(e)
        return null;
      }
  }
  return (
    <>
    <div className="camcont">
      <div className="home">
        <div className="head">
          <div className="heading">
            <div className="head1">HEALTHCARE SEC</div>
            <div className="head2">CAMSEC.AI</div>
          </div>
        </div>
        <hr id="hr"/>
      </div>
      <div className="camset">
      <div className="camsetting">
        <div className="setting-card" style={{marginLeft:'20px'}}>
          <div className="cam-selc-card" >
            <MDBCard className='cam-selc-card' >
              <MDBCardBody>
                <MDBCardTitle style={{marginBottom:'19px',marginTop:'20px'
                ,fontSize:'15px'}}>Camera Selection</MDBCardTitle>
                <Dropdown daa={daa} setdata={setdata} selected={selected} 
                setSelected={setSelected} />  
                </MDBCardBody>
              </MDBCard>
            </div>
          </div>
          <div className="setting-card" style={{marginLeft:'20px'}}>
          <div className="cam-selc-card">
          <MDBCard className="cam-selc-card">
          <MDBCardBody>
          <MDBCardTitle style={{marginBottom:'19px',marginTop:'20px'
          ,fontSize:'15px'}}>I.P. Name</MDBCardTitle>
          <form >
            <label>  
              <input value={data.ip_name}  onChange={(e)=>setIp(e.target.value)} 
              style={{height:'40px'}} type="text" />
            </label>
              </form>
            </MDBCardBody>
          </MDBCard>
        </div>
          </div>
        </div>
        <div className="camsetting" style={{marginLeft:'40px'}}>
          <div className="setting-card">
            {" "}
            <div className="cam-selc-card">
           <MDBCard className="cam-selc-card">
           <MDBCardBody>
           <MDBCardTitle style={{marginBottom:'19px',marginTop:'20px'
           ,fontSize:'15px'}}>Name</MDBCardTitle>
           <form >
            <label>   
              <input value={data.name} onChange={(e)=>setName(e.target.value)} 
              style={{height:'40px'}} type="text" />
            </label>
          </form>
        </MDBCardBody>
      </MDBCard>
    </div>
    </div>
          <div className="setting-card"style={{marginLeft:'10px'}}>
          <div className="cam-selc-card" >
            <MDBCard className='cam-selc-card ' >
              <MDBCardBody className="card-body">
                <MDBCardTitle style={{marginBottom:'19px',marginTop:'20px'
                ,fontSize:'15px'}}>Assign</MDBCardTitle>
                <Assigndropdown selected={selected1} setSelected={setSelected1} />  
              </MDBCardBody>
            </MDBCard>
         </div> 
        </div>
        </div>
        <div className="camsetting"style={{marginLeft:'40px'}}>
          <div className="setting-card">
          <div className="cam-selc-card">
           <MDBCard className="cam-selc-card">
           <MDBCardBody>
           <MDBCardTitle style={{marginBottom:'19px',marginTop:'20px'
           ,fontSize:'15px'}}>RTSP</MDBCardTitle>
           <form >
              <label>   
                <input value={data.rtsp} onChange={(e)=>setRtsp(e.target.value)} style={{height:'40px'}} type="text" />
              </label>
            </form>
            </MDBCardBody>
            </MDBCard>
          </div>
          </div>
          <div className="setting-card"style={{marginLeft:'10px'}}>
          <div className="cam-selc-card" >
          <MDBCard className='cam-selc-card' >
          <MDBCardBody>
          <MDBCardTitle style={{marginBottom:'19px',marginTop:'20px'
          ,fontSize:'15px'}}>Authority</MDBCardTitle>
          <Authoritydropdown value2={data.type} selected={selected2} setSelected={setSelected2} />  
          </MDBCardBody>
          </MDBCard>
          </div>
          </div>
          <button onClick={()=>handle()} style={{background:'white',color:'black'
          ,height:'49px',marginLeft:'64%',marginTop:'0px',width:'115px',borderRadius:'9px',fontSize:'19px'}}><AiOutlineDownload style={{marginRight:'10px'}} />Save</button>
        </div>  
      </div>
    </div>
     <Stack spacing={2} sx={{ width: '200%' }}>
     <Snackbar
       anchorOrigin={{ vertical, horizontal }}
       open={open}
       onClose={handleClose}
       key={vertical + horizontal}
     ><Alert severity="error">{message}</Alert></Snackbar>
     </Stack>
    </>
  );
};

export default Camerasetting;

import React, { useState,useEffect } from "react";
import Camselection from "./Cameraselection";
import Ipname from "./Ipname/Ipname";
import Name from "./Name/Name";
import Assign from "./Assign/Assign";
import Type from "./Type/Type";
import Authority from "./Authority/Authority";
import Settingcard from "./Settingcard";
import { useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Chip from '@mui/material/Chip';
import {AiOutlineDownload} from "react-icons/all"
import { MDBCard, MDBCardBody, MDBCardTitle } from "mdb-react-ui-kit";
import Assigndropdown from "./Assign/Assigndropdown";
import Authoritydropdown from "./Authority/Authoritydropdown";
import Stack from '@mui/material/Stack';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';
import Dropdown from "../Dropdown";
import { DeleteOutline, PausePresentationTwoTone, SentimentVerySatisfiedSharp, ShowChart, UpdateOutlined } from '@material-ui/icons';
import axios from "axios"
const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

const names = [
  'Fire Alert',
  'Mask Alert',
  'Attendance Monitoring',
  'Fall Alert',
  'Foot Fall Alert',
  'Nursing Staff Monitoring',
  'Social Distaincing',
  'Fight Detection',
  'Face Detection',
];
function getStyles(name, personName, theme) {
  return {
    fontWeight:
      personName.indexOf(name) === -1
        ? theme.typography.fontWeightRegular
        : theme.typography.fontWeightMedium,
  };
}
const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

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
  const theme = useTheme();
  const [personName, setPersonName] = React.useState([]);

  const handleChange = (event) => {
    const {
      target: { value },
    } = event;
    setPersonName(
      // On autofill we get a stringified value.
      typeof value === 'string' ? value.split(',') : value,
    );
  };

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
          <div className="cam-selc-card" style={{height:'10px'}}>
            <MDBCard className='cam-selc-card' >
              <MDBCardBody>
                <MDBCardTitle style={{marginBottom:'19px',marginTop:'20px'
                ,fontSize:'15px',color:'white'}}>Camera Selection</MDBCardTitle>
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
          ,fontSize:'15px',color:'white'}}>I.P. Name</MDBCardTitle>
          <form >
            <label>  
              <input value={data.ip_name}  onChange={(e)=>setIp(e.target.value)} 
              style={{height:'6.3vh'}} type="text" />
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
           <MDBCardTitle style={{marginBottom:'19px',marginTop:'7px'
           ,fontSize:'15px',color:'white'}}>Name</MDBCardTitle>
           <form >
            <label>   
              <input value={data.name} onChange={(e)=>setName(e.target.value)} 
              style={{height:'6.3vh'}} type="text" />
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
                <MDBCardTitle style={{marginBottom:'9px',marginTop:'20px'
                ,fontSize:'15px',color:'white'}}>Assign</MDBCardTitle>     
                {/* <div  style={{height:'7vh',width:'254px',border:'1px solid white'}}>
                */}
                <FormControl sx={{ m: 1, width: 300 }}>
        <Select
          labelId="demo-multiple-chip-label"
          id="demo-multiple-chip"
          style={{background:'white',height:'7vh',width:'20vw'}}
          multiple
          value={personName}
          onChange={handleChange}
          input={<OutlinedInput id="select-multiple-chip" label="Chip" />}
          renderValue={(selected) => (
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
              {selected.map((value) => (
                <Chip key={value} label={value} />
              ))}
            </Box>
          )}
          MenuProps={MenuProps}
        >
          {names.map((name) => (
            <MenuItem
              key={name}
              value={name}
              style={getStyles(name, personName, theme)}
            >
              {name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
              
              
                {/* <Select style={{color:'white',background:'white'}}>
                <div className="dropdown-item">
                  <MenuItem style={{color:'white'}}>ffffffffff</MenuItem>
                  <MenuItem style={{color:'white'}}>ffffffffff</MenuItem>
                  <MenuItem style={{color:'white'}}>ffffffffff</MenuItem>
                  <MenuItem style={{color:'white'}}>ffffffffff</MenuItem>
                  <MenuItem style={{color:'white'}}>ffffffffff</MenuItem>
                  </div>
                </Select> */}

                {/* <select style={{background:'red',border:'18px solid red',height:'1200vh',width:'200px'}}  data-placeholder="Begin typing a name to filter..." multiple class="chosen-select" name="test">
                
                <option value=""></option>
                <option>American Black Bear</option>
                <option>Asiatic Black Bear</option>
                <option>Brown Bear</option>
                <option>Giant Panda</option>
                <option>Sloth Bear</option>
                <option>Sun Bear</option>
                <option>Polar Bear</option>
                <option>Spectacled Bear</option>
  </select> */}

  {/* <input type="submit"/> */}

{/* </div>       */}
        {/* <select>
                <option>gggggg</option>
                <option>gggggg</option><option>gggggg</option><option>gggggg</option>
                </select>  */}
                {/* <Assigndropdown selected={selected1} setSelected={setSelected1} />  
               */}
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
           <MDBCardTitle style={{marginBottom:'19px',marginTop:'7px'
           ,fontSize:'15px',color:'white'}}>RTSP</MDBCardTitle>
           <form >
              <label>   
                <input value={data.rtsp} onChange={(e)=>setRtsp(e.target.value)} style={{height:'6.3vh'}} type="text" />
              </label>
            </form>
            </MDBCardBody>
            </MDBCard>
          </div>
          </div>
          {/* <div className="setting-card"style={{marginLeft:'10px'}}>
          <div className="cam-selc-card" >
          <MDBCard className='cam-selc-card' >
          <MDBCardBody>
          <MDBCardTitle style={{marginBottom:'19px',marginTop:'20px'
          ,fontSize:'15px'}}>Authority</MDBCardTitle>
          <Authoritydropdown value2={data.type} selected={selected2} setSelected={setSelected2} />  
          </MDBCardBody>
          </MDBCard>
          </div>
          </div> */}
          {/* <br></br>
          <br></br>
          <br></br><br></br>
          <br></br>
          <br></br>
          <br></br> */}
          <div style={{display:'flex',flexDirection:'column',marginTop:'14px',marginTop:'30vh'}}>
          <button onClick={()=>handle()} style={{background:'white',color:'black'
          ,height:'49px',marginLeft:'64%',marginTop:'0px',width:'115px',borderRadius:'9px',fontSize:'19px'}}><AiOutlineDownload style={{marginRight:'10px'}} />Save</button>
        </div> 
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

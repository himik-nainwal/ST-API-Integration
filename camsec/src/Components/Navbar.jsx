import React from "react";

import { Link } from "react-router-dom";
import "./Header.css";
import { useLocation } from "react-router-dom";
import logo from "./Images/icon.jfif";
import { ImHome3 } from "react-icons/im";
import { GiCctvCamera } from "react-icons/gi";
import { IoIosAddCircle } from "react-icons/io";
import { BiSelection } from "react-icons/bi";
import { RiNotification2Fill } from "react-icons/ri";
import { VscGraph } from "react-icons/vsc";
import { AiOutlineLogout } from "react-icons/ai";
import { Avatar } from "@mui/material";
import { NavLink } from "react-router-dom";

const Navbar = () => {
  const location = useLocation();

  //destructuring pathname from location
  const { pathname } = location;

  //Javascript split method to get the name of the path in array
  const splitLocation = pathname.split("/");
  return (
    <div className="nav_head s" >
      <div className="imgcontainer n1" >
        <Avatar style={{background:'white',color:'black',width:'10vh'
        ,height:'10vh'}} src={logo} alt="Logo" />
       </div>
         <b className="bha">Bharat Kushwaha</b>
          <hr width='100%' size={4} color='black'></hr>
        
          {splitLocation[1] === "home"?
           <Link  className="text-link"  to="/home">
            <div style={{marginTop:'20px'}} className="textlink1">
             <div className="d2">  
            <font className='d1'>
              <ImHome3 style={{marginRight:'10px',fontSize:'23px'
              ,marginTop:'14px',borderRadius:'400px'}} /><b style={{marginTop:'15px',textDecoration:
              'none',background:'rgba(122, 123, 116, 0.72)',color:'black'}}>
              Home</b></font>
              </div>
           </div>
      </Link>:
        <Link className="text-link"  to="/home">
        <div className="textlink2">
         <div className="pl1">
        <font className='pl2'><ImHome3 className="pl3" />
        <p style={{marginTop:'15px',textDecoration: 'none',background:'white'
        ,color:'black',fontWeight:'400px'}}>Home</p></font></div>
      </div>
     </Link>
    }
      {splitLocation[1] === "Camerasetting"?
        <Link className="text-link"  to="/Camerasetting">
            <div className="textlink1">
             <div className="d2">  
            <font className='d1'>
              <GiCctvCamera style={{marginRight:'10px',fontSize:'23px'
              ,marginTop:'14px',borderRadius:'400px'}} /><b style={{marginTop:'15px',textDecoration:
              'none',background:'rgba(122, 123, 116, 0.72)',color:'black'}}>
              Camera Setting</b></font>
              </div>
           </div>
      </Link>:
        <Link className="text-link"  to="/Camerasetting">
        <div className="textlink2">
         <div className="pl1">
        <font className='pl2'><GiCctvCamera className="pl3" />
        <p style={{marginTop:'15px',textDecoration: 'none',background:'white'
        ,color:'black',fontWeight:'400px'}}>Camera Setting</p></font></div>
  </div>
  </Link>
    }
     {splitLocation[1] === "AddUser"?
        <Link className="text-link"  to="/AddUser">
            <div className="textlink1">
             <div className="d2">  
            <font className='d1'>
              <IoIosAddCircle style={{marginRight:'10px',fontSize:'23px'
              ,marginTop:'14px',borderRadius:'400px'}} /><b style={{marginTop:'15px',textDecoration:
              'none',background:'rgba(122, 123, 116, 0.72)',color:'black'}}>
              Add User</b></font>
              </div>
           </div>
      </Link>:
        <Link className="text-link"  to="/AddUser">
        <div className="textlink2">
         <div className="pl1">
        <font className='pl2'><IoIosAddCircle className="pl3" />
        <p style={{marginTop:'15px',textDecoration: 'none',background:'white'
        ,color:'black',fontWeight:'400px'}}>Add User</p></font></div>
  </div>
  </Link>
    }
    {splitLocation[1] === "Areaselection"?
        <Link className="text-link"  to="/Areaselection">
            <div className="textlink1">
             <div className="d2">  
            <font className='d1'>
              <BiSelection style={{marginRight:'10px',fontSize:'23px'
              ,marginTop:'14px',borderRadius:'400px'}} /><b style={{marginTop:'15px',textDecoration:
              'none',background:'rgba(122, 123, 116, 0.72)',color:'black'}}>
              Area Selection</b></font>
              </div>
           </div>
      </Link>:
        <Link className="text-link"  to="/Areaselection">
        <div className="textlink2">
         <div className="pl1">
        <font className='pl2'><BiSelection className="pl3" />
        <p style={{marginTop:'15px',textDecoration: 'none',background:'white'
        ,color:'black',fontWeight:'400px'}}>Area Selection</p></font></div>
  </div>
  </Link>
    }
       {splitLocation[1] === "Eventoccur"?
        <Link className="text-link"  to="/Eventoccur">
            <div className="textlink1">
             <div className="d2">  
            <font className='d1'>
              <RiNotification2Fill style={{marginRight:'10px',fontSize:'23px'
              ,marginTop:'14px',borderRadius:'400px'}} /><b style={{marginTop:'15px',textDecoration:
              'none',background:'rgba(122, 123, 116, 0.72)',color:'black'}}>
             Event Occurence</b></font>
              </div>
           </div>
      </Link>:
        <Link className="text-link"  to="/Eventoccur">
        <div className="textlink2">
         <div className="pl1">
        <font className='pl2'><RiNotification2Fill className="pl3" />
        <p style={{marginTop:'15px',textDecoration: 'none',background:'white'
        ,color:'black',fontWeight:'400px'}}>Event Occurence</p></font></div>
  </div>
  </Link>
    }

{splitLocation[1] === " Visulization"?
        <Link className="text-link"  to="/Visulization">
            <div className="textlink1">
             <div className="d2">  
            <font className='d1'>
              <VscGraph style={{marginRight:'10px',fontSize:'23px'
              ,marginTop:'14px',borderRadius:'400px'}} /><b style={{marginTop:'15px',textDecoration:
              'none',background:'rgba(122, 123, 116, 0.72)',color:'black'}}>
              Visulization</b></font>
              </div>
           </div>
      </Link>:
        <Link className="text-link"  to="/Visulization">
        <div className="textlink2">
         <div className="pl1">
        <font className='pl2'>
          <VscGraph className="pl3" />
        <p style={{marginTop:'15px',textDecoration: 'none',background:'white'
        ,color:'black',fontWeight:'400px'}}> Visulization</p></font></div>
  </div>
  </Link>
    }
       {/* {splitLocation[1] === "Eventoccur"?
        <Link className="text-link"  to="/Eventoccur">
            <div className="textlink1">
             <div className="d2">  
            <font className='d1'>
              <RiNotification2Fill style={{marginRight:'10px',fontSize:'23px'
              ,marginTop:'14px'}} /><b style={{marginTop:'15px',textDecoration:
              'none',background:'rgba(122, 123, 116, 0.72)',color:'black'}}>
             Event Occurence</b></font>
              </div>
           </div>
      </Link>:
        <Link className="text-link"  to="/Eventoccur">
        <div className="textlink2">
         <div className="pl1">
        <font className='pl2'><RiNotification2Fill className="pl3" />
        <p style={{marginTop:'15px',textDecoration: 'none',background:'white'
        ,color:'black',fontWeight:'400px'}}>Event Occurence</p></font></div>
  </div>
  </Link>
    } */}

{splitLocation[1] === "/"?
        <Link className="text-link"  to="/">
            <div className="textlink1">
             <div className="d2">  
            <font className='d1'>
              <AiOutlineLogout style={{marginRight:'10px',fontSize:'23px'
              ,marginTop:'14px',borderRadius:'400px'}} /><b style={{marginTop:'15px',textDecoration:
              'none',background:'rgba(122, 123, 116, 0.72)',color:'black'}}>
              Logout</b></font>
              </div>
           </div>
      </Link>:
        <Link className="text-link"  to="/">
        <div className="textlink2">
         <div className="pl1">
        <font className='pl2'><AiOutlineLogout className="pl3" />
        <p style={{marginTop:'15px',textDecoration: 'none',background:'white'
        ,color:'black',fontWeight:'400px'}}> Logout</p></font></div>
  </div>
  </Link>
    }
{/*       
      <p className="nav_list"style={{background:'white',marginTop:'30px'
       ,color:'black'}}>
        <AiOutlineLogout className="ico" style={{background:'',fontSize:'20px'
         ,color:'black'}}/>
        Logout
      </p> */}
    </div>
  );
};

export default Navbar;

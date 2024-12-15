import numpy as np
import math
import random
import os
import csv

class Flow:
    def __init__(self, idx, service_type, dis, SNR, pkg_number, pkg_size, state_id_SNR, state_id_pkg_size, state_id_pkg_number, state_id_distance, data_rate,state_id, C_alloc, B_alloc, delay_requirement,delay=0):
        self.idx = idx
        self.service_type = service_type
        self.c_calculated = 0
        self.state_id_SNR = state_id_SNR
        self.state_id_pkg_size = state_id_pkg_size
        self.state_id_pkg_number = state_id_pkg_number
        self.SNR=SNR 
        self.pkg_number=pkg_number
        self.pkg_size=pkg_size
        self.Bandwidth_allocated = B_alloc
        self.Compute_allocated = C_alloc
        self.delay_requirement = delay_requirement
        self.delay=delay
        self.global_state_id=state_id
        self.distance = dis
        self.state_id_distance=state_id_distance
        self.data_rate = data_rate


    def state_update(self):
        pass


class Environ:
    def __init__(self, flow_number_highest, flow_number_lowest, path, time_stamp):
        self.flow_number_highest=flow_number_highest # 7 # make sure flow number within 2~6
        self.flow_number_lowest=flow_number_lowest # 2
        # self.core_node_number = core_node_number # 2,3,4
        self.eMBB_throu_lower = 0.3 # Gbps
        self.eMBB_comp_lower = 2 # Gbps
        self.eMBB_mem_lower = 2 # Gb
        self.eMBB_delay = 20/1000 # s
        self.URLLC_throu_lower = 2.08 # Gbps
        self.URLLC_comp_lower = 1 # Gbps
        self.URLLC_mem_lower = 1 # Gb
        self.URLLC_delay = 1/1000 # s
        self.eMBB_throu_upper = 30.5 # Gbps
        self.eMBB_comp_upper = 40 # Gbps
        self.eMBB_mem_upper = 50 # Gb
        self.URLLC_throu_upper = 10 # Gbps
        self.URLLC_comp_upper = 100 # Gbps
        self.URLLC_mem_upper = 100 # Gb
        self.Link_Bl = 50 # Gbps
        self.AccessNode_Cm = 30 # Gb
        self.CoreNode_Cm = 70 # Gb
        self.AccessNode_Cc = 30 # Gb
        self.CoreNode_Cc = 60 # Gb
        self.node_type_list=[0,0,0,0,0,0,1,1,1]
        # self.node_type_list=[0,0]
        self.Ts = 0.2# s
        self.classified_state=[]
        self.time_stamp=time_stamp
        self.state_number = 10
        self.resource_list  = []
        self.compute_allocated = 0
        self.compute_required=np.random.rand()*5+30
        self.save_path = path
        self.next_state_list=[]
        self.f_c = 3e9
        self.Los_sys = 10**(0.1/10)
        self.c=299792458
        self.nLos_sys = 10**(3.5/10)
        self.noise_density = 10**(-143/10)*1e-3
        self.pi=3.1415926535898
        self.P=1.7 #w

        self.total_SNR_states_slice_1 = np.array([10,25,20.5,32,33.4, 22,30,25.5,25,15])+np.random.rand(10,)*5 #SNR slice URLLC
        self.total_SNR_states_slice_2 = np.array([15,33,20.5,26,29, 20,25,17,25,15])+np.random.rand(10,)*5 #SNR slice eMBB
        # # self.total_distance_states_slice_2 = np.array([420,450,430,470,480,500,430,450,435,480])+np.random.rand(10,)*20 #SNR slice URLLC
        # self.total_distance_states_slice_1 = np.array([450,440,450,460,420,470,460,480,410,440])+np.random.rand(10,)*5 #SNR slice eMBB
        self.total_distance_states_slice_2 = np.array([450,450,450,450,450,450,450,450,450,450])*1.8+np.random.rand(10,)*2 #SNR slice URLLC
        self.total_distance_states_slice_1 = np.array([450,450,450,450,450,450,450,450,450,450])*1.8+np.random.rand(10,)*2 #SNR slice eMBB
        self.total_data_rate_states_slice_1 = np.array([40,40,40,40,40,20,20,20,20,20])
        self.total_data_rate_states_slice_2 = np.array([20,20,20,20,20,5,5,5,5,5])

        self.total_packet_number_states_slice_1 = np.array([100,100,100,100,100, 100,100,100,100,100])//3+np.round(np.random.rand(10,)*25) #packet number slice URLLC
        self.total_packet_size_states_slice_1 = np.array([100,100,100,100,100, 100,100,100,100,100])/100000+np.random.rand(10,)*0.002 #packet size mber slice URLLC Mb
        self.total_packet_number_states_slice_2 = np.array([100,100,100,100,100, 100,100,100,100,100])//3+np.round(np.random.rand(10,)*25) #packet number slice EMBB
        self.total_packet_size_states_slice_2 = np.array([100,100,100,100,100, 100,100,100,100,100])/1000+np.random.rand(10,)*0.2 #packet size mber slice EMBB Mb
        self.delay_requirement=np.array([0.001, 0.1]) # delay request for URLLC and eMBB
        self.transition_matrix_SNR = self.generate_transition_matrix_SNR(self.state_number)
        self.transition_matrix_pkt_size = self.generate_transition_matrix_pkt_size(self.state_number)
        self.transition_matrix_pkt_number = self.generate_transition_matrix_pkt_number(self.state_number)
        self.transition_matrix = self.generate_transition_matrix_SNR(self.state_number)

        self.action_dim=4 # for both agent, for user admission 0~8 is the number of the user to be admitted, for resource agent, 3 by 3 number of combination
        # self.compute_capacity = 1600 #Mbps
        # self.bandwidth_capacity = 1600 #Mbps 
        self.compute_capacity = 300 #Mbps
        self.bandwidth_capacity = 300 #Mbps 

    def generate_transition_matrix_SNR(self, num_states):
        P = np.zeros((num_states, num_states))
        for i in range(num_states):
            P[i][i] = 0.8  # Transition to the left state
            if i < num_states-1 :
                P[i][i+1] = 0.2  # Transition to the right state
            if i == num_states-1 :
                P[i][0] =0.2

        return P


    def generate_transition_matrix_pkt_size(self, num_states):
        P = np.zeros((num_states, num_states))
        for i in range(num_states):
            P[i][i] = 0.8  # Transition to the left state
            if i < num_states-1 :
                P[i][i+1] = 0.2  # Transition to the right state
            if i == num_states-1 :
                P[i][0] =0.2

        return P

    def generate_transition_matrix_pkt_number(self, num_states):
        P = np.zeros((num_states, num_states))
        for i in range(num_states):
            P[i][i] = 0.8  # Transition to the left state
            if i < num_states-1 :
                P[i][i+1] = 0.2  # Transition to the right state
            if i == num_states-1 :
                P[i][0] =0.2

        return P

    def reward_func_ra(self, data_rate, request_data_rate): #energy_efficiency_thresh=31.5, lambda=0.1 for resource=600, 700, 800, 900, lambda=0.1 for resource=1000, 1100, 1200, 1300
        slope=100
        p=0.2
        # R_1 =1 / (1 + np.exp(-0.8 * (data_rate[0]-request_data_rate[0] + 0)))
         
        R_1 =-(data_rate[0]-request_data_rate[0] + 0)**2
        if data_rate[0]>request_data_rate[0]:
            R_1=0
        

        # R_2 =1 / (1 + np.exp(-0.8 * (data_rate[1]-request_data_rate[1] + 0)))
        R_2 =-(data_rate[1]-request_data_rate[1] + 0)**2
        if data_rate[1]>request_data_rate[1]:
            R_2=R_2*5


        R = R_1*(1-p)+R_2*p
        return R


    def step(self, Action, ts,option):
        step_size=5
        if Action==0:
           add_resource_bandwidth_UE1 = step_size
           add_resource_bandwidth_UE2 = -step_size
        if Action==1:
           add_resource_bandwidth_UE1 = step_size
           add_resource_bandwidth_UE2 = step_size
        if Action==2:
           add_resource_bandwidth_UE1 = -step_size
           add_resource_bandwidth_UE2 = -step_size
        if Action==3:
           add_resource_bandwidth_UE1 = -step_size
           add_resource_bandwidth_UE2 = step_size
        # if Action==4:
        #    add_resource_bandwidth_UE1 = 0
        #    add_resource_bandwidth_UE2 = -step_size
        # # if Action==5:
        #    add_resource_bandwidth_UE1 = 0
        #    add_resource_bandwidth_UE2 = step_size
        # if Action==6:
        #    add_resource_bandwidth_UE1 = -step_size
        #    add_resource_bandwidth_UE2 = -0
        # if Action==7:
        #    add_resource_bandwidth_UE1 = -step_size
        #    add_resource_bandwidth_UE2 = 0
        # if Action==8:
        #    add_resource_bandwidth_UE1 = -0
        #    add_resource_bandwidth_UE2 = 0



        SNR_array = np.array(self.SNR_list)
        Bandwidth_resource_allocation=np.array([add_resource_bandwidth_UE1, add_resource_bandwidth_UE2])
        # upate resource allocation
        self.bandwidth_allocated += Bandwidth_resource_allocation
        # perform clipping
        self.bandwidth_allocated = np.clip(self.bandwidth_allocated, 1, self.bandwidth_capacity)

        self.bandwidth_allocated = np.round(np.clip(self.bandwidth_capacity/(np.sum(self.bandwidth_allocated)+0.0001), 0.0001, 1)*self.bandwidth_allocated)
        self.data_rate = self.bandwidth_allocated * np.log2(1 + SNR_array)
        self.request_data_rate = np.array([self.flow_list[0].data_rate, self.flow_list[1].data_rate])
        self.reward_ra= self.reward_func_ra(self.data_rate, self.request_data_rate)
        reward_array = self.reward_ra
        # calculate the metrics
        if option=='train' and ts>=self.time_stamp-1:
            delay_violation_rate = np.array(self.delay_violation_rate)
            total_drop_instance_array = np.array(self.total_drop_rate_list)
            energy_efficiency_array = np.array(self.energy_efficiency_list)
            
            save_path_resources = os.path.join(self.save_path, 'delay_violation_rate')
            with open(save_path_resources  +'_'+ option+'.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(delay_violation_rate)
            save_path_resources_1 = os.path.join(self.save_path, 'number_of_packet_drop')
            with open(save_path_resources_1  +'_'+ option+'.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(total_drop_instance_array)
            save_path_resources_2 = os.path.join(self.save_path, 'energy_efficiency')
            with open(save_path_resources_2  +'_'+ option+'.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(energy_efficiency_array)
            save_path_resources_3 = os.path.join(self.save_path, 'reward_array')
            with open(save_path_resources_3  +'_'+ option+'.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(reward_array)
        else:
            save_path_resources_3 = os.path.join(self.save_path, 'reward_array')
            reward_array = np.array([reward_array])
            with open(save_path_resources_3  +'_'+ option+'.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(reward_array)

        # state transition
        if option=='test' or option=='train':
            num_states_SNR = len(self.transition_matrix_SNR)

            for phi in range(len(self.flow_list)):
                flow = self.flow_list[phi]
                flow.global_state_id = np.random.choice(num_states_SNR, p=self.transition_matrix[flow.global_state_id])
                flow.state_id_SNR = flow.global_state_id 
                flow.state_id_pkg_size = flow.global_state_id 
                flow.state_id_pkg_number = flow.global_state_id 
                flow.state_id_distance = flow.global_state_id 
                flow.state_id_request_data_rate = flow.global_state_id 

                if flow.service_type==0:
                   flow.pkg_size =  self.total_packet_size_states_slice_1[flow.state_id_pkg_size]
                   flow.pkg_number =  self.total_packet_number_states_slice_1[flow.state_id_pkg_number]
                   flow.distance =  self.total_distance_states_slice_1[flow.state_id_distance]
                   flow.data_rate =  self.total_data_rate_states_slice_1[ flow.state_id_request_data_rate]

                else:
                   flow.pkg_size =  self.total_packet_size_states_slice_2[flow.state_id_pkg_size]
                   flow.pkg_number =  self.total_packet_number_states_slice_2[flow.state_id_pkg_number]
                   flow.distance =  self.total_distance_states_slice_2[flow.state_id_distance]
                   flow.data_rate =  self.total_data_rate_states_slice_2[ flow.state_id_request_data_rate]



        self.SNR_list=[]
        self.distance_list=[]
        self.pkg_size_list=[]
        self.pkg_number_list=[]
        self.delay_request_list=[]
        self.data_rate_request_list=[]
        number_of_flow=len(self.flow_list)

        for psi in range(number_of_flow):

            self.distance_list.append(self.flow_list[psi].distance)

            self.pkg_size_list.append(self.flow_list[psi].pkg_size)
            self.pkg_number_list.append(self.flow_list[psi].pkg_number)
            self.delay_request_list.append(self.flow_list[psi].delay_requirement)
            self.data_rate_request_list.append(self.flow_list[psi].data_rate)

        # SNR_array=np.array(self.SNR_list)
        distance_array=np.array(self.distance_list)
        Path_loss_array = 20*np.log10(4*self.pi*self.f_c*distance_array/self.c)+self.Los_sys
        SNR_array = self.P*10**(-Path_loss_array/10)/(self.noise_density*(self.bandwidth_allocated*1e6))
        self.SNR_list = SNR_array.tolist()
        self.data_rate = np.round(self.bandwidth_allocated * np.log2(1 + SNR_array),2)
        data_rate_UE1 = self.data_rate[0]
        data_rate_UE2 = self.data_rate[1]
        bandwidth_UE1, bandwidth_UE2 = self.bandwidth_allocated[0], self.bandwidth_allocated[1]

        self.states_array_ra = [data_rate_UE1, data_rate_UE2]+self.data_rate_request_list
        save_path_resources_4= os.path.join(self.save_path, 'resource_allocation')
        resource_allocation=np.array(self.states_array_ra+[bandwidth_UE1, bandwidth_UE2])
        with open(save_path_resources_4  +'_'+ option+'.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(resource_allocation)


        self.reward_ra=np.round(self.reward_ra,3)
        s_next_list = self.states_array_ra
        r_list = [self.reward_ra]
        return s_next_list, r_list

    def reset(self, flow_list, eps):
        self.total_drop_rate_list=[]
        self.SNR_list=[]
        self.distance_list=[]
        self.pkg_size_list=[]
        self.pkg_number_list=[]
        self.delay_request_list=[]
        self.data_rate_request_list=[]
        number_of_flow=len(flow_list)

        for psi in range(number_of_flow):

            self.distance_list.append(flow_list[psi].distance)
            # self.SNR_list.append(flow_list[psi].SNR)
            self.pkg_size_list.append(flow_list[psi].pkg_size)
            self.pkg_number_list.append(flow_list[psi].pkg_number)
            self.delay_request_list.append(flow_list[psi].delay_requirement)
            self.data_rate_request_list.append(self.flow_list[psi].data_rate)

        distance_array=np.array(self.distance_list)

        Path_loss_array = 20*np.log10(4*self.pi*self.f_c*distance_array/self.c)+self.Los_sys
        SNR_array = self.P*10**(-Path_loss_array/10)/(self.noise_density*self.bandwidth_allocated*1e6)
        self.SNR_list = SNR_array.tolist()
        self.data_rate = np.round(self.bandwidth_allocated * np.log2(1 + SNR_array),3)
        data_rate_UE1 = self.data_rate[0]
        data_rate_UE2 = self.data_rate[1]
        self.bandwidth_allocated = np.clip(self.bandwidth_allocated, 1, self.bandwidth_capacity)

        # bandwidth_UE1, bandwidth_UE2 = self.bandwidth_allocated[0], self.bandwidth_allocated[1]
        self.states_array_ra = [data_rate_UE1, data_rate_UE2]+self.data_rate_request_list
        state_list = [self.states_array_ra]
        return state_list

    def Reset(self,option=None,eps=None):
        # np.random.seed(eps) 

        service_type=0
        service_type=0
        # resource_capacity_list=[200,250,300,350,400,450,500,550,600,650,700,750,800]
        self.flow_list=[]

        self.bandwidth_allocated = np.array([30,30])
        number_of_flow=2
        for phi in range(number_of_flow):
            state_id_SNR= np.random.randint(0,10) 
            state_id_pkg_size= np.random.randint(0,10) 
            state_id_pkg_number= np.random.randint(0,10)
            state_id_distance= np.random.randint(0,10)
            state_id = np.random.randint(0,10)
            if service_type==0: # 0 is the eMBB
                SNR = self.total_SNR_states_slice_1[state_id_SNR]
                pkg_number = self.total_packet_number_states_slice_1[state_id_pkg_size]
                pkg_size  = self.total_packet_size_states_slice_1[state_id_pkg_number]
                distance = self.total_distance_states_slice_1[state_id_SNR]
                data_rate_request =self.total_data_rate_states_slice_1[state_id_SNR]

            elif service_type==1: # 1 is the URLLC
                SNR = self.total_SNR_states_slice_2[state_id_SNR]
                pkg_number = self.total_packet_number_states_slice_2[state_id_pkg_size]
                pkg_size  = self.total_packet_size_states_slice_2[state_id_pkg_number]
                distance = self.total_distance_states_slice_2[state_id_SNR]
                data_rate_request =self.total_data_rate_states_slice_2[state_id_SNR]

                # self.next_state_list.append(np.random.choice(num_states, p=self.transition_matrix[self.current_state_slice_2]))
            else:
                raise Exception("The slice type you have entered is not considered")
            B_alloc =  self.bandwidth_allocated[phi]
            delay_requirement=self.delay_requirement[service_type]
            C_alloc=0
            self.flow_list.append(Flow(phi, service_type,distance, SNR, pkg_number, pkg_size, state_id_SNR, state_id_pkg_size, state_id_pkg_number, state_id_distance, data_rate_request, state_id, C_alloc, B_alloc, delay_requirement))
            if service_type==0:
               service_type=1
            else: 
               service_type=0

        s=self.reset(self.flow_list, eps)
        # s_list = s.tolist()
        s_list = s


        return s_list

    def randsample(self):
        return np.random.randint(0,self.action_dim)




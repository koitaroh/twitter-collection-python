#!/usr/bin/env python
# encoding: utf-8

import os
import time
import csv
import numpy as np

alpha = 0.001
beta = 0.001
gamma = 0.001

T = 48
D = 7
K = 10
R = 5
M = 365*T

NUM_ITERATION = 50
NUM_USERS = 1000

locations = []
users = []
data = []

def readOneUser(full_path):
    user_id = 0
    start_time = time.mktime(time.strptime('2010-08-01 00:00:00','%Y-%m-%d %H:%M:%S'))
    with open(full_path,'r') as f:
        isFirst = True
        user_index = -1
        for id_str, time_str, lat_str, lon_str, errlevel_str, vel_str, pre_str, city_str in csv.reader(f):
            if isFirst:
                user_id = int(id_str)
                if user_id not in users:
                    users.append(user_id)
                user_index = users.index(user_id)
                isFirst = False

            cur_time = time.mktime(time.strptime(time_str,'%Y-%m-%d %H:%M:%S'))
            dis_time = int( ( cur_time - start_time ) / 1800 )
            if dis_time < 0:
                continue
            dis_lat = int( ( float( lat_str ) - 35.0 ) / 0.008 )
            dis_lon = int( ( float( lon_str ) - 139.0 ) / 0.010 )
            if (dis_lat,dis_lon) not in locations:
                locations.append((dis_lat,dis_lon))
            loc_index = locations.index((dis_lat,dis_lon))
            data.append((user_index,dis_time,loc_index))

    print '{} Read Complete.'.format(full_path)

def readData(dirpath):
    cnt = 0
    for filename in os.listdir(dirpath):
        cnt += 1
        if cnt > NUM_USERS:
            break

        full_path = os.path.join(dirpath,filename)
        if os.path.isdir(full_path):
            print full_path
            continue
        elif os.path.isfile(full_path):
            print 'Read {}'.format(full_path)
            readOneUser(full_path)
        else:
            print 'Unidentified name {}.'.format(full_path)

def sample_index(p):
    return np.random.multinomial(1,p).argmax()

def conditional_distribution(ntk,ndk,nulk,nuk,nk,nu,ntr,nlr,nur,nr,u,d,t,l,dt):
    p_theta = ( nuk[u,:] + alpha ) / ( nu[u] + K * alpha )
    p_t = ( ntk[t,:] + beta ) / ( nk + T * beta )
    p_d = ( ndk[d,:] + beta ) / ( nk + D * beta )
    p_phi = ( nulk[u,l,:] + gamma ) / ( nuk[u,:] + len(locations) * gamma )
    p_k = p_theta * p_t * p_d * p_phi

    p_theta = ( nur[u,:] + alpha ) / ( nu[u] + K * alpha )
    p_t = ( ntr[dt,:] + beta ) / ( nr + M * beta )
    p_phi = ( nlr[l,:] + gamma ) / ( nur[u,:] + len(locations) * gamma )
    p_r = p_theta * p_t * p_phi

    p_kr = np.concatenate((p_k,p_r),axis=0)
    p_kr /= np.sum( p_kr )
    return p_kr

def crowdtopic():
    U = len(users)
    L = len(locations)
    N = len(data)

    topics = np.zeros(N,dtype=np.int32)

    ntk = np.zeros((T,K),dtype=np.int32)
    ndk = np.zeros((D,K),dtype=np.int32)
    nulk = np.zeros((U,L,K),dtype=np.int32)
    nuk = np.zeros((U,K),dtype=np.int32)
    nk = np.zeros(K,dtype=np.int32)
    nu = np.zeros(U,dtype=np.int32)
    ntr = np.zeros((M,R),dtype=np.int32)
    nlr = np.zeros((L,R),dtype=np.int32)
    nur = np.zeros((U,R),dtype=np.int32)
    nr = np.zeros(R,dtype=np.int32)

    for i in xrange(N):
        u,dt,l = data[i]
        t = dt % T
        d = ( dt / T ) % D
        s = np.random.randint(2)
        if s==0:
            k = np.random.randint(K)
            ntk[(t,k)] += 1
            ndk[(d,k)] += 1
            nulk[(u,l,k)] += 1
            nuk[(u,k)] += 1
            nk[k] += 1
            nu[u] += 1
            topics[i] = k
        else:
            r = np.random.randint(R)
            ntr[(dt,r)] += 1
            nlr[(l,r)] += 1
            nur[(u,r)] += 1
            nr[r] += 1
            nu[u] += 1
            topics[i] = K+r

    for i in xrange(NUM_ITERATION):
        print 'Iteration {}'.format(i)
        for i in xrange(N):
            u,dt,l = data[i]
            t = dt % 48
            d = ( dt / 48 ) % 7
            kr = topics[i]
            if kr < K:
                k = kr
                ntk[(t,k)] -= 1
                ndk[(d,k)] -= 1
                nulk[(u,l,k)] -= 1
                nuk[(u,k)] -= 1
                nk[k] -= 1
            else:
                r = kr-K
                ntr[(dt,r)] -= 1
                nlr[(l,r)] -= 1
                nur[(u,r)] -= 1
                nr[r] -= 1

            p_kr = conditional_distribution(ntk,ndk,nulk,nuk,nk,nu,ntr,nlr,nur,nr,u,d,t,l,dt)
            kr = sample_index(p_kr)

            if kr < K:
                k = kr
                topics[i] = k
                ntk[(t,k)] += 1
                ndk[(d,k)] += 1
                nulk[(u,l,k)] += 1
                nuk[(u,k)] += 1
                nk[k] += 1
            else:
                r = kr-K
                topics[i] = K+r
                ntr[(dt,r)] += 1
                nlr[(l,r)] += 1
                nur[(u,r)] += 1
                nr[r] += 1

    return ntk,ndk,nulk,nuk,ntr,nlr,nur

def main():
    readData('/media/fan/65D42DD030E60A2D/ZDC/ID/1352090540/1352090540')
    ntk,ndk,nulk,nuk,ntr,nlr,nur = crowdtopic()
    np.savetxt( 'ntk.csv' , ntk , delimiter=',' )
    np.savetxt( 'ndk.csv' , ndk , delimiter=',' )
    for i in xrange(len(users)):
        np.savetxt( '{}.csv'.format(users[i]) , nulk[i,:,:] , delimiter=',' )
    with open('user_index.csv','w') as f:
        for i in xrange(len(users)):
            f.write('{},{}\n'.format(i,users[i]))
    with open('location_index.csv','w') as f:
        for i in xrange(len(locations)):
            dis_lat,dis_lon = locations[i]
            f.write('{},{},{}\n'.format(i,dis_lat,dis_lon))
    np.savetxt( 'nuk.csv' , nuk , delimiter=',' )
    np.savetxt( 'nur.csv' , nur , delimiter=',' )
    np.savetxt( 'ntr.csv' , ntr , delimiter=',' )
    np.savetxt( 'nlr.csv' , nlr , delimiter=',' )

if __name__ == '__main__':
    main()

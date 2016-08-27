from app.settings import *
import pygame

class CollisionPlayerPlatform:
    def __init__(self, player, map):
        # self.soundControl = soundPlayerController
        self.tileWidth = map.tmxData.tilewidth
        self.tileHeight = map.tmxData.tileheight
        self.mapHeight = map.tmxData.height * self.tileHeight
        self.mapWidth = map.tmxData.width * self.tileWidth
        self.player = player
        self.map = map

    def collisionAllSprites(self, player, mapData, gameData):
        for sprite in mapData.allSprites:
            if sprite.isPhysicsApplied == True or sprite.isCollisionApplied == True:

                self.rightCollision(sprite, mapData)
                self.downCollision(sprite, mapData)
                self.leftCollision(sprite, mapData)
                self.upCollision(sprite, mapData)

                self.collisionWithEnemy(player, mapData.enemyGroup)
                self.pickUpItem(player, mapData.itemGroup, gameData)

    def rightCollision(self,player, map):

        # mapHeight = map.tmxData.height * tileHeight
        i=0

        if player.rect.right + player.speedx > 0:
            if player.speedx >= self.tileWidth: #Si on va plus vite qu'une tile/seconde
                while player.rect.right+i*self.tileWidth < player.rect.right + player.speedx:
                    if player.rect.right+i*self.tileWidth >= self.mapWidth:
                        j=0
                        while map.tmxData.get_tile_gid((self.mapWidth - 1 - j*self.tileWidth)/self.tileWidth, player.rect.top/self.tileHeight, COLLISION_LAYER) == SOLID and map.tmxData.get_tile_gid((self.mapWidth - 1- j*self.tileWidth)/self.tileWidth, (player.rect.bottom)/self.tileHeight, COLLISION_LAYER) == SOLID:
                            j += 1
                        player.rect.right = self.mapWidth-j*self.tileWidth-1
                        player.speedx = 0
                        return

                    upRightTileGid = map.tmxData.get_tile_gid((player.rect.right + i*self.tileWidth)/self.tileWidth, player.rect.top/self.tileHeight, COLLISION_LAYER)
                    downRightTileGid = map.tmxData.get_tile_gid((player.rect.right + i*self.tileWidth)/self.tileWidth, (player.rect.bottom-1)/self.tileHeight, COLLISION_LAYER)

                    if (upRightTileGid  == SOLID or downRightTileGid  == SOLID) and player.speedx > 0 and player.facingSide == RIGHT:
                        while map.tmxData.get_tile_gid((player.rect.right + 1)/self.tileWidth, player.rect.top/self.tileHeight, COLLISION_LAYER) != SOLID and map.tmxData.get_tile_gid((player.rect.right + 1)/self.tileWidth, (player.rect.bottom-1)/self.tileHeight, COLLISION_LAYER) != SOLID:
                            player.rect.right += 1
                        player.speedx = 0
                    i += 1

            else:
                upRightTileGid = self.map.tmxData.get_tile_gid((player.rect.right + player.speedx)/self.tileWidth, player.rect.top/self.tileHeight, COLLISION_LAYER)
                downRightTileGid = self.map.tmxData.get_tile_gid((player.rect.right + player.speedx)/self.tileWidth, (player.rect.bottom-1)/self.tileHeight, COLLISION_LAYER)
                lowMidRightTileGid = self.map.tmxData.get_tile_gid((player.rect.right + player.speedx)/self.tileWidth, (player.rect.centery-10-1)/self.tileHeight, COLLISION_LAYER)
                highMidRightTileGid = self.map.tmxData.get_tile_gid((player.rect.right + player.speedx)/self.tileWidth, (player.rect.centery+10-1)/self.tileHeight, COLLISION_LAYER)

                if (upRightTileGid  == SOLID or downRightTileGid == SOLID or lowMidRightTileGid == SOLID or highMidRightTileGid == SOLID) and player.speedx > 0:
                    # while map.tmxData.get_tile_gid((player.rect.right + 1)/self.tileWidth, player.rect.top/self.tileHeight, COLLISION_LAYER) != SOLID and map.tmxData.get_tile_gid((player.rect.right + 1)/self.tileWidth, (player.rect.bottom)/self.tileHeight, COLLISION_LAYER) != SOLID:
                    #     player.rect.right += 1
                    player.speedx = 0
                    player.rect.right += self.tileWidth - (player.rect.right % self.tileWidth) - 1 #On colle le player sur le mur à droite
                elif upRightTileGid  == SPIKE or downRightTileGid == SPIKE or lowMidRightTileGid == SPIKE or highMidRightTileGid == SPIKE:
                    player.dead()
                elif (upRightTileGid  == SPRING or downRightTileGid == SPRING or lowMidRightTileGid == SPRING or highMidRightTileGid == SPRING) and player.speedx > 0:
                    player.speedx = 0

    def getUpRightTileGid(self):
        return self.map.tmxData.get_tile_gid((self.player.rect.right + self.player.speedx)/self.tileWidth, self.player.rect.top/self.tileHeight, COLLISION_LAYER)
    def getDownRightTileGid(self):
        return self.map.tmxData.get_tile_gid((self.player.rect.right + self.player.speedx)/self.tileWidth, (self.player.rect.bottom-1)/self.tileHeight, COLLISION_LAYER)
    def getLowMidRightTileGid(self):
        return self.map.tmxData.get_tile_gid((self.player.rect.right + self.player.speedx)/self.tileWidth, (self.player.rect.centery-10-1)/self.tileHeight, COLLISION_LAYER)
    def getHighMidRightTileGid(self):
        return self.map.tmxData.get_tile_gid((self.player.rect.right + self.player.speedx)/self.tileWidth, (self.player.rect.centery+10-1)/self.tileHeight, COLLISION_LAYER)
    # def getRightTilesList(self): à terminer si besoin (décomposer le nb de pts de vérification sur le sprite selon sa taille, à place de 4 fixes)
    #     tileList = []
    #     pointNumber = self.tileHeight
    #     tileList.append(self.map.tmxData.get_tile_gid((self.player.rect.right + self.player.speedx)/self.tileWidth, (self.player.rect.centery+10-1)/self.tileHeight, COLLISION_LAYER))

    def leftCollision(self,player, map):
        tileWidth = map.tmxData.tilewidth
        tileHeight = map.tmxData.tileheight
        # mapWidth = map.tmxData.width * tileWidth
        # mapHeight = map.tmxData.height * tileHeight
        i = 0

        if -player.speedx >= tileWidth:
            while player.rect.x-i*tileWidth > player.rect.x + player.speedx:
                if player.rect.x-i*tileWidth <= 0:
                    j=0
                    while map.tmxData.get_tile_gid((0 + j*tileWidth)/tileWidth, player.rect.top/tileHeight, COLLISION_LAYER) == SOLID and map.tmxData.get_tile_gid((0 + j*tileWidth)/tileWidth, (player.rect.bottom-1)/tileHeight, COLLISION_LAYER) == SOLID:
                        j += 1
                    player.rect.left = j*tileWidth
                    player.speedx = 0
                    return

                upLeftTileGid = map.tmxData.get_tile_gid((player.rect.left - i*tileWidth)/tileWidth, player.rect.top/tileHeight, COLLISION_LAYER)
                downLeftTileGid = map.tmxData.get_tile_gid((player.rect.left - i*tileWidth)/tileWidth, (player.rect.bottom-1)/tileHeight, COLLISION_LAYER)

                if (upLeftTileGid  == SOLID or downLeftTileGid  == SOLID) and player.facingSide == LEFT:
                    while map.tmxData.get_tile_gid((player.rect.left)/tileWidth, player.rect.top/tileHeight, COLLISION_LAYER) != SOLID and map.tmxData.get_tile_gid((player.rect.left)/tileWidth, (player.rect.bottom-1)/tileHeight, COLLISION_LAYER) != SOLID:
                        player.rect.left -= 1
                    player.speedx = 0
                i += 1

        else:
            upLeftTileGid = map.tmxData.get_tile_gid((player.rect.left + player.speedx)/tileWidth, player.rect.top/tileHeight, COLLISION_LAYER)
            downLeftTileGid = map.tmxData.get_tile_gid((player.rect.left + player.speedx)/tileWidth, (player.rect.bottom-1)/tileHeight, COLLISION_LAYER)
            lowMidLeftTileGid = map.tmxData.get_tile_gid((player.rect.left + player.speedx)/tileWidth, (player.rect.centery-10)/tileHeight, COLLISION_LAYER)
            highMidLeftTileGid = map.tmxData.get_tile_gid((player.rect.left + player.speedx)/tileWidth, (player.rect.centery+10)/tileHeight, COLLISION_LAYER)

            if (upLeftTileGid  == SOLID or downLeftTileGid  == SOLID or lowMidLeftTileGid == SOLID or highMidLeftTileGid == SOLID) and player.speedx < 0:
                #while map.tmxData.get_tile_gid((player.rect.left)/tileWidth, player.rect.top/tileHeight, COLLISION_LAYER) != SOLID and map.tmxData.get_tile_gid((player.rect.left)/tileWidth, (player.rect.bottom-1)/tileHeight, COLLISION_LAYER) != SOLID:
                     #player.rect.left -= 1
                player.speedx = 0
                player.rect.left -= (player.rect.left % self.tileWidth) #On colle le player sur le mur de gauche
            elif upLeftTileGid  == SPIKE or downLeftTileGid  == SPIKE or lowMidLeftTileGid == SPIKE or highMidLeftTileGid == SPIKE:
                player.dead()
            elif (upLeftTileGid  == SPRING or downLeftTileGid  == SPRING or lowMidLeftTileGid == SPRING or highMidLeftTileGid == SPRING) and player.speedx < 0:
                player.speedx = 0

    def downCollision(self,player, map):
        tileWidth = map.tmxData.tilewidth
        tileHeight = map.tmxData.tileheight
        # mapWidth = map.tmxData.width * tileWidth
        # mapHeight = map.tmxData.height * tileHeight

        downLeftTileGid = map.tmxData.get_tile_gid((player.rect.left+1)/tileWidth, (player.rect.bottom + player.speedy)/tileHeight, COLLISION_LAYER)
        downRightTileGid = map.tmxData.get_tile_gid((player.rect.right)/tileWidth, (player.rect.bottom + player.speedy)/tileHeight, COLLISION_LAYER)
        downMidTileGID = map.tmxData.get_tile_gid((player.rect.centerx)/tileWidth, (player.rect.bottom + player.speedy)/tileHeight, COLLISION_LAYER)

        if downLeftTileGid == SOLID or downRightTileGid == SOLID or downMidTileGID == SOLID:
            # while map.tmxData.get_tile_gid((player.rect.left+1)/tileWidth, (player.rect.bottom)/tileHeight, COLLISION_LAYER) != SOLID and map.tmxData.get_tile_gid((player.rect.right)/tileWidth, (player.rect.bottom)/tileHeight, COLLISION_LAYER) != SOLID:
            #     player.rect.bottom += 1
            player.speedy = 0
            player.jumpState = GROUNDED
        elif downLeftTileGid == SPIKE or downRightTileGid == SPIKE  or downMidTileGID == SPIKE:
            player.dead()
        elif downLeftTileGid == SPRING or downRightTileGid == SPRING  or downMidTileGID == SPRING:
            player.spring()
        else:
            if player.jumpState == GROUNDED:
                player.jumpState = JUMP


    def upCollision(self,player, map):
        tileWidth = map.tmxData.tilewidth
        tileHeight = map.tmxData.tileheight

        upLeftTileGid = map.tmxData.get_tile_gid((player.rect.left+1)/tileWidth, (player.rect.top + player.speedy)/tileHeight, COLLISION_LAYER)
        upRightTileGid = map.tmxData.get_tile_gid(player.rect.right/tileWidth, (player.rect.top + player.speedy)/tileHeight, COLLISION_LAYER)
        upMidTileGid = map.tmxData.get_tile_gid(player.rect.centerx/tileWidth, (player.rect.top + player.speedy)/tileHeight, COLLISION_LAYER)

        if upLeftTileGid == SOLID or upRightTileGid == SOLID or upMidTileGid == SOLID:
            #Coller le player sur le plafond
            while map.tmxData.get_tile_gid((player.rect.left+1)/tileWidth, (player.rect.top)/tileHeight, COLLISION_LAYER) != SOLID and map.tmxData.get_tile_gid(player.rect.right/tileWidth, (player.rect.top)/tileHeight, COLLISION_LAYER) != SOLID:
                player.rect.bottom -= 1

            player.rect.bottom += 1 #Redescendre de 1 pour sortir du plafond
            player.speedy = 0
        elif upLeftTileGid == SPIKE or upRightTileGid == SPIKE:
            player.dead()

    def collisionWithEnemy(self, player, enemyGroup):
        collisionList = pygame.sprite.spritecollide(player, enemyGroup, False)
        for enemy in collisionList:
            player.dead()
            # player.loseLife()
            # self.soundControl.hurt()
            pass

    def pickUpItem(self, player, itemGroup, gameMemory):
        collisionList = pygame.sprite.spritecollide(player, itemGroup, False)
        for item in collisionList:
            gameMemory.registerItemPickedUp(item)
            item.kill()

def collisionBulletWall(bullet, map):
    tileWidth = map.tmxData.tilewidth
    tileHeight = map.tmxData.tileheight
    mapWidth = map.tmxData.width * tileWidth
    mapHeight = map.tmxData.height * tileHeight

    if (bullet.rect.top < tileHeight or bullet.rect.bottom > mapHeight - tileHeight) or (bullet.rect.left < tileWidth or bullet.rect.right > mapWidth - tileWidth):
        bullet.kill()
        return

    if bullet.speedx > 0:
        upRightTileGid = map.tmxData.get_tile_gid((bullet.rect.right + bullet.speedx)/tileWidth, bullet.rect.top/tileHeight, COLLISION_LAYER)
        downRightTileGid = map.tmxData.get_tile_gid((bullet.rect.right + bullet.speedx)/tileWidth, (bullet.rect.bottom-1)/tileHeight, COLLISION_LAYER)

        if (upRightTileGid  == SOLID or downRightTileGid  == SOLID):
            bullet.kill()

    elif bullet.speedx < 0:
        upLeftTileGid = map.tmxData.get_tile_gid((bullet.rect.left + bullet.speedx)/tileWidth, bullet.rect.top/tileHeight, COLLISION_LAYER)
        downLeftTileGid = map.tmxData.get_tile_gid((bullet.rect.left + bullet.speedx)/tileWidth, (bullet.rect.bottom)/tileHeight, COLLISION_LAYER)

        if (upLeftTileGid  == SOLID or downLeftTileGid  == SOLID) and bullet.speedx < 0:
            bullet.kill()

    if (bullet.rect.top < tileHeight or bullet.rect.bottom > mapHeight - tileHeight) or (bullet.rect.left < tileWidth or bullet.rect.right > mapWidth - tileWidth):
        bullet.kill()
        return

    if bullet.speedx > 0:
        upRightTileGid = map.tmxData.get_tile_gid((bullet.rect.right + bullet.speedx)/tileWidth, bullet.rect.top/tileHeight, COLLISION_LAYER)
        downRightTileGid = map.tmxData.get_tile_gid((bullet.rect.right + bullet.speedx)/tileWidth, (bullet.rect.bottom-1)/tileHeight, COLLISION_LAYER)

        if (upRightTileGid  == SOLID or downRightTileGid  == SOLID):
            bullet.kill()

    elif bullet.speedx < 0:
        upLeftTileGid = map.tmxData.get_tile_gid((bullet.rect.left + bullet.speedx)/tileWidth, bullet.rect.top/tileHeight, COLLISION_LAYER)
        downLeftTileGid = map.tmxData.get_tile_gid((bullet.rect.left + bullet.speedx)/tileWidth, (bullet.rect.bottom)/tileHeight, COLLISION_LAYER)

        if (upLeftTileGid  == SOLID or downLeftTileGid  == SOLID) and bullet.speedx < 0:
            bullet.kill()

def collisionBulletEnemy(bullet, map):
    collisionList = pygame.sprite.spritecollide(bullet, map.enemyGroup, False)
    for enemy in collisionList:
        enemy.dead()
        bullet.kill()

def collisionBulletPlayer(map, player):
    collisionList = pygame.sprite.spritecollide(player, map.enemyBullet, False)
    for bullet in collisionList:
        player.dead()
        bullet.kill()

def printTile(tile):
    if tile == SOLID:
        print('SOLID')
    elif tile == SPIKE:
        print('SPIKE')
    elif tile == SPRING:
        print('SPRING')
    else:
        print(tile)

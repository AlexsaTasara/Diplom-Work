import indexes as ind
from objects import *
from maps import *
from mainCharacter import *
from sprites import *
from strings import *
from constants import *
from sqlite3 import Date

# Этот файл подлежит будущему удалению.

spawTime = mapW[ind.mapNo] * mapH[ind.mapNo] / 100
def drawGame():
    if ctx == None:
        return
    if not isAllLoaded:
        requestAnimationFrame(drawGame)
        return
    currentFrameTime = Date.now()
    timeElapsed = currentFrameTime - lastFrameTime
    ind.gameTime += math.floor(timeElapsed * ind.gameSpeeds[currentSpeed].mult)
    sec = math.floor(Date.now() / 1000)
    if sec != ind.currentSecond:
        ind.currentSecond = sec
        ind.framesLastSecond = ind.frameCount
        ind.frameCount = 1
    else:
        ind.frameCount += 1
    if (keysDown[16]):
        player.delayMove = 75
    else:
        player.delayMove = 150
    if (!mapChange & !player.processMovement(gameTime) & gameSpeeds[currentSpeed].mult != 0):
        if (keysDown[38] | keysDown[87]):
            if (player.direction != directions.up):
                player.direction = directions.up
            else:
                if (player.canMoveUp()):
                    player.MoveUp(gameTime)
    else:
        if (keysDown[40] | keysDown[83]):
            if (player.direction != directions.down):
                player.direction = directions.down
            else:
                if (player.canMoveDown()):
                    player.MoveDown(gameTime);
        else:
            if (keysDown[39] | keysDown[68]):
                if (player.direction != directions.right):
                    player.direction = directions.right
                else:
                    if (player.canMoveRight()):
                        player.MoveRight(gameTime)
            else:
                if (keysDown[37] | keysDown[65]):
                    if (player.direction != directions.left):
                        player.direction = directions.left
                    else:
                        if (player.canMoveLeft()):
                            player.MoveLeft(gameTime)
    if heroVisible:
        viewport.update(
        player.position[0] + (player.dimensions[0] / 2),
        player.position[1] + (player.dimensions[1] / 2),
        )
    else:
        viewport.update(
        ((mapW[mapNo] - 1) * tileW) / 2 + (tileW * (mapW[mapNo] % 2) / 2),
        ((mapH[mapNo] - 1) * tileH) / 2 + (tileH * (mapH[mapNo] % 2) / 2),
        );

    ctx.fillStyle = '#424242'
    ctx.fillRect(0, 0, viewport.screen[0], viewport.screen[1])

    for (let z = 0; z < mapTileData[mapNo].layer; z++):
        for (let y = viewport.startTile[1]; y <= viewport.endTile[1]; y++):
            for (let x = viewport.startTile[0]; x <= viewport.endTile[0]; x++):
                if (z == 0):
                    ctx.drawImage(tileTypes[mapTileData[mapNo].map[toIndex(x, y)].type].sprite,
                    viewport.offset[0] + x * tileW,
                    viewport.offset[1] + y * tileH,
                    tileW, tileH)
                else:
                    if (z == 1):
                        iss = mapTileData[mapNo].map[toIndex(x, y)].itemStack
                        if ( iss != null):
                            sprite = itemTypes[iss.type].sprite
                            ctx.drawImage(tileset, sprite[0].x, sprite[0].y,
                            sprite[0].w, sptite[0].h,
                            viewport.offset[0] + (x * tileW) + itemTypes[iss.type].offset[0],
                            viewport.offset[1] + (y * tileH) + itemTypes[iss.type].offset[1],
                            sprite[0].w, sprite[0].h)
                obj = mapTileData[mapNo].map[toIndex(x, y)].object;
                plant111 = mapTileData[ind.mapNo].map[toIndex(x, y)].plant
                anim111 = mapTileData[ind.mapNo].map[toIndex(x, y)].animal
                if (obj != null & obj.objectTypes[obj.type].zIndex == z):
                    objTypes = obj.objectTypes[obj.type];
                    ctx.drawImage(objTypes.sp,
                    objTypes.sprite[0].x, objTypes.sprite[0].y,
                    objTypes.sprite[0].w, objTypes.sprite[0].h,
                    viewport.offset[0] + (x * ind.tileW) + objTypes.offset[0],
                    viewport.offset[1] + (y * ind.tileH) + objTypes.offset[1],
                    objTypes.sprite[0].w, objTypes.sprite[0].h);
                if plant111 != null & z == 1:
                    pInd = eco.lookPlant(plant111.index);
                    sPlant = eco.plants[pInd];
                    plantSprite = sPlant.sprites[sPlant.status];
                    ctx.drawImage(plantDraw,
                    plantSprite[0].x, plantSprite[0].y,
                    plantSprite[0].w, plantSprite[0].h,
                    viewport.offset[0] + (x * ind.tileW),
                    viewport.offset[1] + (y * ind.tileH),
                    plantSprite[0].w, plantSprite[0].h);
                if anim111 != null & z == 1:
                    aInd = eco.lookAnim(anim111.index);
                    sAnim = eco.animals[aInd];
                    aColor = eco.animals[aInd].color;
                    # console.log(sAnim.spriteDirect);
                    animSprite = sAnim.sprites[sAnim.spriteDirect];
                    ctx.drawImage(animalDraw,
                    animSprite[0].x, animSprite[0].y,
                    animSprite[0].w, animSprite[0].h,
                    viewport.offset[0] + (x * tileW),
                    viewport.offset[1] + (y * tileH),
                    animSprite[0].w, animSprite[0].h);
                    imageData = ctx.getImageData(viewport.offset[0] + (x * tileW), viewport.offset[1] + (y * tileH), 40, 40);

                    # проверяем каждый пиксель,
                    # меняем старый rgb на новый
                    for (i=0; i < imageData.data.length;i += 4):
                        ccr = imageData.data[i];
                        ccg = imageData.data[i+1];
                        ccb = imageData.data[i+2];
                        if ((ccr >= 160 & & ccr <= 250) & (ccg >= 160 & ccg <= 250) & & (ccb >= 160 & ccb <= 250)):
                            cr = Math.floor(ccr / 255 * aColor[0]);
                            cg = Math.floor(ccg / 255 * aColor[1]);
                            cb = Math.floor(ccb / 255 * aColor[2]);
                            imageData.data[i]= cr;
                            imageData.data[i+1]= cg;
                            imageData.data[i+2]= cb;
                    ctx.putImageData(imageData, viewport.offset[0] + (x * tileW), viewport.offset[1] + (y * tileH));
        if (z == 1 & heroVisible):
            sprite = player.sprites[player.direction];
            ctx.drawImage(hero,
            sprite[0].x, sprite[0].y,
            sprite[0].w, sprite[0].h,
            viewport.offset[0] + player.position[0],
            viewport.offset[1] + player.position[1] - 10,
            player.dimensions[0], player.dimensions[1])

        if ((z == 3) & (clientSpawn | objectSpawn | animalSpawn | plantSpawn)):
            sprite = curs.sprite;
            ctx.drawImage(cursorDraw, 0, 0, 40, 40,
            viewport.offset[0] + curs.tileTo[0] * tileW,
            viewport.offset[1] + curs.tileTo[1] * tileH,
            tileW, tileH);

    ctx.textAlign = "left";
    ctx.font = "bold 40pt helvetica";
    ctx.fillStyle = "#f90606";
    if (gameSpeeds[currentSpeed].name == "Paused"):
        ctx.fillText(stmodstat1[userLang], viewport.screen[0] / 2 - 40, 50);
    else:
        ctx.fillText(stmodstat2[userLang], viewport.screen[0] / 2 - 40, 50);

    ctx.fillStyle = '#ffffff';
    ctx.font = "bold 15pt helvetica";

    ctx.fillText(stControl1[userLang], 10, 20);
    ctx.fillText(stControl2[userLang], 10, 40);
    ctx.fillText(stControl3[userLang], 10, 60);
    ctx.fillText(stControl4[userLang], 10, 80);
    ctx.fillText(stControl5[userLang], 10, 100);
    ctx.fillText(stControl6[userLang], 10, 120);
    ctx.fillText(stControl7[userLang], 10, 140);
    ctx.fillText(stControl8[userLang], 10, 160);
    ctx.fillText(stControl9[userLang], 10, 180);
    ctx.fillText(stControl12[userLang], 10, 200);
    ctx.fillText(stControl10[userLang] + gameSpeeds[currentSpeed].name, 10, viewport.screen[1] - 60);
    ctx.fillText(stControl11[userLang], 10, viewport.screen[1] - 40);
    ctx.font = "bold 20pt helvetica";
    ctx.fillText(stAnimCount[userLang] + eco.animals.length, viewport.screen[0] - 425, 40);
    ctx.fillText(stPlSL[userLang] + stPlS[PLT][userLang], viewport.screen[0] - 875, viewport.screen[1] - 50);
    ctx.fillText(stPlSW[userLang] + stPlS[PLW][userLang], viewport.screen[0] - 875, viewport.screen[1] - 20);

    if (mapChange):
        ctx.fillStyle = '#000000';
        ctx.fillRect(viewport.screen[0] / 2 - 220, viewport.screen[1] / 2 - 280, 480, 280);
        ctx.font = 'bold 13pt helvetica';
        ctx.fillStyle = '#dbdbdb';
        ctx.fillText(stchosemapInf[userLang], viewport.screen[0] / 2 - 200, viewport.screen[1] / 2 - 250);
        switch(mapCh):
            case 0:
                ctx.fillText(stmapchoice0, viewport.screen[0] / 2 - 200, viewport.screen[1] / 2 - 220);
                break;
            case 1:
                ctx.fillText(stmapchoice1, viewport.screen[0] / 2 - 200, viewport.screen[1] / 2 - 220);
                break;
            case 2:
                ctx.fillText(stmapchoice2, viewport.screen[0] / 2 - 200, viewport.screen[1] / 2 - 220);
                break;
            case 3:
                ctx.fillText(stmapchoice3, viewport.screen[0] / 2 - 200, viewport.screen[1] / 2 - 220);
                break
            case 4:
                ctx.fillText(stmapchoice4, viewport.screen[0] / 2 - 200, viewport.screen[1] / 2 - 220);
                break
            case 5:
                ctx.fillText(stmapchoice5, viewport.screen[0] / 2 - 200, viewport.screen[1] / 2 - 220);
                break
            case 6:
                ctx.fillText(stmapchoice6, viewport.screen[0] / 2 - 200, viewport.screen[1] / 2 - 220);
                break
            case 7:
                ctx.fillText(stmapchoice7, viewport.screen[0] / 2 - 200, viewport.screen[1] / 2 - 220);
                break
            case 8:
                ctx.fillText(stmapchoice8, viewport.screen[0] / 2 - 200, viewport.screen[1] / 2 - 220);
                break
            case 9:
                ctx.fillText(stmapchoice9, viewport.screen[0] / 2 - 200, viewport.screen[1] / 2 - 220);
                break
        ctx.fillText(stwi[userLang] + mapW[mapCh], viewport.screen[0] / 2 - 200, viewport.screen[1] / 2 - 190);
        ctx.fillText(sthe[userLang] + mapH[mapCh], viewport.screen[0] / 2 - 200, viewport.screen[1] / 2 - 160);
        ctx.fillText(stmapchchose[userLang], viewport.screen[0] / 2 - 200, viewport.screen[1] / 2 - 20);

    ctx.font = "bold 20pt helvetica";
    ctx.fillStyle = "#b296fd";
    if (clientSpawn){
        ctx.fillText(stUser[userLang], viewport.screen[0] / 2 - 160, 80);
    }
    if (objectSpawn){
        ctx.fillText(stObject[userLang], viewport.screen[0] / 2-220, 80);
    }
    if (plantSpawn){
        ctx.fillText(stPlant[userLang], viewport.screen[0] / 2-220, 80);
        ctx.fillText(stPlantt[userLang] + stplantType[et][userLang], viewport.screen[0] / 2-225, 110);
        ctx.fillStyle = '#ffffff';
        ctx.font = "bold 15pt helvetica";
        ctx.fillText(stTypeCh[userLang], 10, 220);
        ctx.font = "bold 20pt helvetica";
        ctx.fillStyle = "#b296fd";
    }
    if (animalSpawn){
        ctx.fillText(stanimal1[userLang], viewport.screen[0] / 2-225, 80);
        ctx.fillText(stAnimCol[userLang] + stCol[chosenColorInd][userLang], viewport.screen[0] / 2-225, 110);
        ctx.fillText(stAnimt[userLang] + stanimType[et][userLang], viewport.screen[0] / 2-225, 140);
        ctx.fillStyle = '#ffffff';
        ctx.font = "bold 15pt helvetica";
        ctx.fillText(stAnimColContr[userLang], 10, 220);
        ctx.fillText(stTypeCh[userLang], 10, 240);
        ctx.font = "bold 20pt helvetica";
        ctx.fillStyle = "#b296fd";
    }

    if (info) {
        ctx.fillText(stAInf0[userLang], viewport.screen[0] / 2-225, 80);
        if (animInfo){
            aI = eco.lookAnim(amInfInd);
            if (aI >= 0){
                ctx.fillStyle = '#000000';
                ctx.fillRect(100, 100, 450, 280);
                ctx.font = 'bold 25pt helvetica';
                ctx.fillStyle = '#dbdbdb';
                ctx.fillText(stAInf0[userLang], 120, 145);
                ctx.font = 'bold 15pt helvetica';
                ctx.fillText(stAInf1[userLang] + eco.animals[aI].index, 120, 180);
                ctx.fillText(stAInf2[userLang] + eco.animals[aI].color, 120, 200);
                ctx.fillText(stAnimt[userLang] + stanimType[eco.animals[aI].ecoT][userLang], 120, 220);
                ctx.fillText(stAInf3[userLang] + eco.animals[aI].liveTime, 120, 240);
                ctx.fillText(stAInf4[userLang] + eco.animals[aI].told, 120, 260);
                ctx.fillText(stAInf5[userLang] + eco.animals[aI].energy, 120, 280);
                ctx.fillText(stAInf6[userLang] + eco.animals[aI].startEnergy, 120, 300);
                ctx.fillText(stAInf7[userLang] + eco.animals[aI].maxEnergy, 120, 320);
                const sprite = curs.sprite;
                ctx.drawImage(cursorDraw,
                0, 0, 40, 40,
                viewport.offset[0] + eco.animals[aI].tileTo[0] * tileW,
                viewport.offset[1] + eco.animals[aI].tileTo[1] * tileH,
                tileW, tileH);
            } else {
                animInfo = false;
            }
        }
    }

    if (tTime >= timeEcosystem){
        tPlantL++;
        tPlantW++
        if (PLT == 2){
            point = RandomPoint(mapNo, ecoType.Land, eco);
            if (point[0] != [0] & & point[1] != [0]){
                eco.addPlant(point[0], point[1], ecoType.Land);
            }
        } else if (PLT > 2){
            for (let m = 2; m < PLT+1;m++){
                let point = RandomPoint(mapNo, ecoType.Land);
                if (point[0] !=[0] & & point[1] !=[0]){
                    eco.addPlant(point[0], point[1], ecoType.Land);
                }
            }
        } else if (tPlantL > (2 - PLT)){
            tPlantL = 0;
            point = RandomPoint(mapNo, ecoType.Land);
            if (point[0] != [0] & & point[1] != [0]){
                eco.addPlant(point[0], point[1], ecoType.Land);
            }
        }
        if (PLW == 2){
            point = RandomPoint(mapNo, ecoType.Water);
            if (point[0] != [0] & & point[1] != [0]){
                eco.addPlant(point[0], point[1], ecoType.Water)
            }
        } else
        if (PLW > 2){
            for (let m = 2; m < PLW+1;m++):
                point = RandomPoint(mapNo, ecoType.Water);
                if (point[0] !=[0] & & point[1] !=[0]):
                    eco.addPlant(point[0], point[1], ecoType.Water)
        } else:
            if (tPlantW > (2 - PLW)):
                tPlantW = 0
                point = RandomPoint(mapNo, ecoType.Water)
                if (point[0] != [0] & & point[1] != [0]):
                    eco.addPlant(point[0], point[1], ecoType.Water)
            h = 0
            for (h=0; h < eco.plants.length; h++):
                if (!eco.plants[h].timeUpdate()):
                    eco.delPlant(eco.plants[h].index)
                    h--
                    continue
                eco.plants[h].statusUpdate()
            tTime = 0
            for (h=0; h < eco.animals.length; h++):
                eco.animals[h].tileFrom = eco.animals[h].tileTo
                eco.animals[h].courseLast = eco.animals[h].courseNext
            for (h=0; h < eco.animals.length; h++):
                if (!eco.animals[h].timeUpdate()):
                    eco.delAnim(eco.animals[h].index)
                    h -= 1
                    continue
                stat = eco.animals[h].status
                if stat != statusAnim.ZERO & stat != statusAnim.DEATH:
                    view.updateLook(eco.animals[h].tileFrom, eco.animals[h].ecoT, eco)
                    view.updateLists(eco.animals[h].myCourse(), eco.animals[h].tileFrom, eco)
                    stat = eco.choosePurpose(h)
            tTime = 0
        }
        tTime += Math.floor(timeElapsed * gameSpeeds[currentSpeed].mult)
        lastFrameTime = currentFrameTime
        requestAnimationFrame(drawGame)